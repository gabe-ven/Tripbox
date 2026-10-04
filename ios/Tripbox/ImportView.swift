import SwiftUI

struct ImportView: View {
    var body: some View {
        ContentUnavailableView(
            "Import Screenshots",
            systemImage: "photo.on.rectangle",
            description: Text("Screenshot import is coming soon.")
        )
        .navigationTitle("Import")
    }
}

#Preview {
    NavigationStack { ImportView() }
}
