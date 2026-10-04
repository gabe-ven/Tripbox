import SwiftUI

struct BackendStatusView: View {
    enum Status {
        case loading
        case connected(String)
        case failed(String)
    }

    @State private var status: Status = .loading
    private let client = APIClient()

    var body: some View {
        HStack {
            switch status {
            case .loading:
                ProgressView()
                Text("Checking server…")
            case .connected(let message):
                Label("Server: \(message)", systemImage: "checkmark.circle.fill")
                    .foregroundStyle(.green)
            case .failed(let message):
                Label(message, systemImage: "exclamationmark.triangle.fill")
                    .foregroundStyle(.red)
                Spacer()
                Button("Retry") {
                    Task { await check() }
                }
            }
        }
        .task { await check() }
    }

    private func check() async {
        status = .loading
        do {
            let response = try await client.health()
            status = .connected(response.status)
        } catch {
            status = .failed(error.localizedDescription)
        }
    }
}
