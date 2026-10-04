import SwiftUI

struct HomeView: View {
    var body: some View {
        NavigationStack {
            List {
                Section {
                    BackendStatusView()
                }

                Section {
                    NavigationLink("Import Screenshot") {
                        ImportView()
                    }
                    NavigationLink("Sample Trip") {
                        TripView()
                    }
                }
            }
            .navigationTitle("Tripbox")
        }
    }
}

#Preview {
    HomeView()
}
