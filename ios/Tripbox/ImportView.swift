import PhotosUI
import SwiftUI

struct ImportView: View {
    enum LoadState {
        case empty
        case loading
        case loaded(SelectedScreenshot)
        case failed(String)
    }

    @State private var selection: PhotosPickerItem?
    @State private var state: LoadState = .empty

    var body: some View {
        content
            .navigationTitle("Import")
            .task(id: selection) { await loadSelection() }
    }

    @ViewBuilder
    private var content: some View {
        switch state {
        case .empty:
            ContentUnavailableView {
                Label("Import a Screenshot", systemImage: "photo.on.rectangle")
            } description: {
                Text("Choose a travel screenshot from your photo library.")
            } actions: {
                picker("Choose Screenshot")
            }

        case .loading:
            ProgressView("Loading screenshot…")

        case .loaded(let screenshot):
            VStack(spacing: 16) {
                Image(uiImage: screenshot.image)
                    .resizable()
                    .scaledToFit()
                    .clipShape(RoundedRectangle(cornerRadius: 12))
                    .frame(maxHeight: .infinity)
                picker("Choose a Different Screenshot")
            }
            .padding()

        case .failed(let message):
            ContentUnavailableView {
                Label("Couldn't Load Screenshot", systemImage: "exclamationmark.triangle")
            } description: {
                Text(message)
            } actions: {
                picker("Choose Another Screenshot")
            }
        }
    }

    private func picker(_ title: String) -> some View {
        PhotosPicker(title, selection: $selection, matching: .images)
            .buttonStyle(.borderedProminent)
    }

    private func loadSelection() async {
        guard let selection else { return }
        state = .loading
        do {
            let screenshot = try await SelectedScreenshot.load(from: selection)
            // A newer selection cancels this task; don't let a stale result overwrite it.
            guard !Task.isCancelled else { return }
            state = .loaded(screenshot)
        } catch {
            guard !Task.isCancelled else { return }
            state = .failed(error.localizedDescription)
        }
    }
}

#Preview {
    NavigationStack { ImportView() }
}
