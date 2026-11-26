import Foundation
import AVFoundation
import ImageIO
import UniformTypeIdentifiers

let args = CommandLine.arguments
guard args.count >= 4 else {
    print("usage: extract_frames <video> <outdir> <seconds...>")
    exit(1)
}
let videoPath = args[1]
let outDir = args[2]
let times = args[3...].compactMap { Double($0) }
let url = URL(fileURLWithPath: videoPath)
let asset = AVURLAsset(url: url)
let sem = DispatchSemaphore(value: 0)

Task {
    do {
        let duration = try await asset.load(.duration)
        print("duration=\(CMTimeGetSeconds(duration))")
        let tracks = try await asset.load(.tracks)
        for t in tracks {
            let type = t.mediaType.rawValue
            let size = try? await t.load(.naturalSize)
            let rate = try? await t.load(.nominalFrameRate)
            print("track \(type) size=\(String(describing: size)) fps=\(String(describing: rate))")
        }
        let gen = AVAssetImageGenerator(asset: asset)
        gen.appliesPreferredTrackTransform = true
        gen.requestedTimeToleranceBefore = .zero
        gen.requestedTimeToleranceAfter = .zero
        try FileManager.default.createDirectory(atPath: outDir, withIntermediateDirectories: true)
        for sec in times {
            let time = CMTime(seconds: sec, preferredTimescale: 600)
            do {
                let (cg, actual) = try await gen.image(at: time)
                let name = String(format: "%@/t%05.1f.png", outDir, sec)
                let dest = CGImageDestinationCreateWithURL(URL(fileURLWithPath: name) as CFURL, UTType.png.identifier as CFString, 1, nil)!
                CGImageDestinationAddImage(dest, cg, nil)
                CGImageDestinationFinalize(dest)
                print("wrote \(name) actual=\(CMTimeGetSeconds(actual)) size=\(cg.width)x\(cg.height)")
            } catch {
                print("fail \(sec): \(error)")
            }
        }
    } catch {
        print("error: \(error)")
    }
    sem.signal()
}
sem.wait()
