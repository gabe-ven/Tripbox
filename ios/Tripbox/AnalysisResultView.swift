import SwiftUI

struct AnalysisResultView: View {
    let analysis: ScreenshotAnalysis

    var body: some View {
        if analysis.travelRelated, let placeName = analysis.placeName {
            VStack(alignment: .leading, spacing: 6) {
                Text(placeName)
                    .font(.title2.bold())
                if let location {
                    Label(location, systemImage: "mappin.and.ellipse")
                }
                if let category = analysis.category {
                    Label(category, systemImage: "tag")
                }
                if let confidence = analysis.confidence {
                    Text("Confidence: \(confidence, format: .percent.precision(.fractionLength(0)))")
                        .font(.footnote)
                        .foregroundStyle(.secondary)
                }
            }
            .frame(maxWidth: .infinity, alignment: .leading)
        } else {
            Label("No travel place found in this screenshot.", systemImage: "questionmark.circle")
                .foregroundStyle(.secondary)
        }
    }

    private var location: String? {
        let parts = [analysis.city, analysis.country].compactMap { $0 }
        return parts.isEmpty ? nil : parts.joined(separator: ", ")
    }
}
