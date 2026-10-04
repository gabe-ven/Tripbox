import PhotosUI
import SwiftUI

struct ImportView: View {
    enum LoadState {
        case empty
        case loading
        case loaded(SelectedScreenshot)
        case failed(String)
    }

    enum AnalysisState {
        case idle
        case analyzing
        case done(ScreenshotAnalysis)
        case failed(String)
    }

    @State private var selection: PhotosPickerItem?
    @State private var state: LoadState = .empty
    @State private var analysis: AnalysisState = .idle
    private let client = APIClient()

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
            ScrollView {
                VStack(spacing: 20) {
                    Image(uiImage: screenshot.image)
                        .resizable()
                        .scaledToFit()
                        .frame(maxHeight: 360)
                        .clipShape(RoundedRectangle(cornerRadius: 12))
                    analysisSection(for: screenshot)
                    picker("Choose a Different Screenshot")
                }
                .padding()
            }

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

    @ViewBuilder
    private func analysisSection(for screenshot: SelectedScreenshot) -> some View {
        switch analysis {
        case .idle:
            EmptyView()
        case .analyzing:
            ProgressView("Finding the place…")
        case .done(let result):
            AnalysisResultView(analysis: result)
        case .failed(let message):
            VStack(spacing: 8) {
                Label(message, systemImage: "exclamationmark.triangle.fill")
                    .foregroundStyle(.red)
                Button("Try Again") {
                    Task { await analyze(screenshot) }
                }
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
        analysis = .idle
        let screenshot: SelectedScreenshot
        do {
            screenshot = try await SelectedScreenshot.load(from: selection)
        } catch {
            // A newer selection cancels this task; don't let a stale result overwrite it.
            guard !Task.isCancelled else { return }
            state = .failed(error.localizedDescription)
            return
        }
        guard !Task.isCancelled else { return }
        state = .loaded(screenshot)
        await analyze(screenshot)
    }

    private func analyze(_ screenshot: SelectedScreenshot) async {
        analysis = .analyzing
        let result: AnalysisState
        do {
            result = .done(try await client.analyzeScreenshot(jpegData: screenshot.uploadData))
        } catch {
            result = .failed(error.localizedDescription)
        }
        // Ignore results for a screenshot that has since been replaced.
        guard case .loaded(let current) = state, current.id == screenshot.id else { return }
        analysis = result
    }
}

#Preview {
    NavigationStack { ImportView() }
}
