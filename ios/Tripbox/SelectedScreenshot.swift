import PhotosUI
import SwiftUI
import UIKit

struct SelectedScreenshot: Identifiable {
    let id = UUID()
    let image: UIImage
    /// JPEG data ready to upload. Re-encoding also drops photo metadata such as location.
    let uploadData: Data

    enum LoadError: LocalizedError {
        case unreadable
        case unsupportedFormat

        var errorDescription: String? {
            switch self {
            case .unreadable:
                return "That photo couldn't be loaded. If it's stored in iCloud, check your connection and try again."
            case .unsupportedFormat:
                return "That file isn't a supported image. Try choosing a different screenshot."
            }
        }
    }

    static func load(from item: PhotosPickerItem) async throws -> SelectedScreenshot {
        let data: Data?
        do {
            data = try await item.loadTransferable(type: Data.self)
        } catch {
            throw LoadError.unreadable
        }

        guard let data else { throw LoadError.unreadable }
        guard let image = UIImage(data: data),
              let uploadData = image.jpegData(compressionQuality: 0.8) else {
            throw LoadError.unsupportedFormat
        }
        return SelectedScreenshot(image: image, uploadData: uploadData)
    }
}
