import Foundation

struct HealthResponse: Decodable {
    let status: String
}

struct ScreenshotAnalysis: Decodable {
    let travelRelated: Bool
    let placeName: String?
    let city: String?
    let country: String?
    let category: String?
    let confidence: Double?
}

enum APIError: LocalizedError {
    case cannotConnect
    case badStatus(Int)
    case server(String)
    case invalidResponse

    var errorDescription: String? {
        switch self {
        case .cannotConnect:
            return "Can't reach the Tripbox server. Make sure the backend is running."
        case .badStatus(let code):
            return "The server returned an error (\(code)). Try again."
        case .server(let message):
            return message
        case .invalidResponse:
            return "The server sent an unexpected response."
        }
    }
}

struct APIClient {
    // The simulator shares the Mac's network, so localhost reaches the local backend.
    // A physical device needs the Mac's LAN IP instead.
    var baseURL = URL(string: "http://127.0.0.1:8000")!
    var session = URLSession.shared

    func health() async throws -> HealthResponse {
        try await send(URLRequest(url: baseURL.appending(path: "health")))
    }

    func analyzeScreenshot(jpegData: Data) async throws -> ScreenshotAnalysis {
        let boundary = "Boundary-\(UUID().uuidString)"
        var request = URLRequest(url: baseURL.appending(path: "analyze-screenshot"))
        request.httpMethod = "POST"
        request.setValue("multipart/form-data; boundary=\(boundary)", forHTTPHeaderField: "Content-Type")

        var body = Data()
        body.append("--\(boundary)\r\n")
        body.append("Content-Disposition: form-data; name=\"file\"; filename=\"screenshot.jpg\"\r\n")
        body.append("Content-Type: image/jpeg\r\n\r\n")
        body.append(jpegData)
        body.append("\r\n--\(boundary)--\r\n")
        request.httpBody = body

        return try await send(request)
    }

    private func send<T: Decodable>(_ request: URLRequest) async throws -> T {
        let data: Data
        let response: URLResponse
        do {
            (data, response) = try await session.data(for: request)
        } catch {
            throw APIError.cannotConnect
        }

        guard let http = response as? HTTPURLResponse else {
            throw APIError.invalidResponse
        }
        guard (200..<300).contains(http.statusCode) else {
            // FastAPI errors look like {"detail": "..."}; surface that message when present.
            if let error = try? JSONDecoder().decode(ErrorResponse.self, from: data) {
                throw APIError.server(error.detail)
            }
            throw APIError.badStatus(http.statusCode)
        }
        do {
            let decoder = JSONDecoder()
            decoder.keyDecodingStrategy = .convertFromSnakeCase
            return try decoder.decode(T.self, from: data)
        } catch {
            throw APIError.invalidResponse
        }
    }
}

private struct ErrorResponse: Decodable {
    let detail: String
}

private extension Data {
    mutating func append(_ string: String) {
        append(Data(string.utf8))
    }
}
