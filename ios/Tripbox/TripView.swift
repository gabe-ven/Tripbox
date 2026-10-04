import SwiftUI

struct TripView: View {
    var body: some View {
        ContentUnavailableView(
            "No Places Yet",
            systemImage: "map",
            description: Text("Places you save will appear here.")
        )
        .navigationTitle("Trip")
    }
}

#Preview {
    NavigationStack { TripView() }
}
