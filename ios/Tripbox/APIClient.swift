import Foundation

struct HealthResponse: Decodable {
    let status: String
}

enum APIError: LocalizedError {
    case cannotConnect
    case badStatus(Int)
    case invalidResponse

    var errorDescription: String? {
        switch self {
        case .cannotConnect:
            return "Can't reach the Tripbox server. Make sure the backend is running."
        case .badStatus(let code):
            return "The server returned an error (\(code)). Try again."
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
        try await get("health")
    }

    private func get<T: Decodable>(_ path: String) async throws -> T {
        let data: Data
        let response: URLResponse
        do {
            (data, response) = try await session.data(from: baseURL.appending(path: path))
        } catch {
            throw APIError.cannotConnect
        }

        guard let http = response as? HTTPURLResponse else {
            throw APIError.invalidResponse
        }
        guard (200..<300).contains(http.statusCode) else {
            throw APIError.badStatus(http.statusCode)
        }
        do {
            return try JSONDecoder().decode(T.self, from: data)
        } catch {
            throw APIError.invalidResponse
        }
    }
}
