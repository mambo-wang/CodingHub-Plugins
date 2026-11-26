import Foundation
import Vision
import AppKit

let args = CommandLine.arguments
guard args.count >= 3 else {
    print("usage: ocr_frames <dir> <out.json> [region y,h]")
    exit(1)
}
let dir = args[1]
let outPath = args[2]
var region: CGRect? = nil
if args.count >= 5, let y = Double(args[3]), let h = Double(args[4]) {
    region = CGRect(x: 0, y: y, width: 1, height: h)
}

let fm = FileManager.default
let files = (try! fm.contentsOfDirectory(atPath: dir))
    .filter { $0.hasSuffix(".png") }
    .sorted { a, b in
        let na = Double(a.dropFirst().split(separator: ".").first ?? "0") ?? 0
        let nb = Double(b.dropFirst().split(separator: ".").first ?? "0") ?? 0
        return na < nb
    }

var results: [[String: Any]] = []
results.reserveCapacity(files.count)

for (idx, f) in files.enumerated() {
    let path = (dir as NSString).appendingPathComponent(f)
    guard let img = NSImage(contentsOfFile: path),
          let tiff = img.tiffRepresentation,
          let rep = NSBitmapImageRep(data: tiff),
          let cg = rep.cgImage else {
        FileHandle.standardError.write("skip \(f)\n".data(using: .utf8)!)
        continue
    }
    var lines: [[String: Any]] = []
    autoreleasepool {
        let handler = VNImageRequestHandler(cgImage: cg, options: [:])
        let req = VNRecognizeTextRequest()
        req.recognitionLevel = .accurate
        req.recognitionLanguages = ["zh-Hans", "en-US"]
        req.usesLanguageCorrection = true
        if let r = region { req.regionOfInterest = r }
        do {
            try handler.perform([req])
            for obs in req.results ?? [] {
                guard let cand = obs.topCandidates(1).first else { continue }
                let b = obs.boundingBox
                lines.append([
                    "text": cand.string,
                    "conf": Double(cand.confidence),
                    "x": Double(b.origin.x),
                    "y": Double(b.origin.y),
                    "w": Double(b.size.width),
                    "h": Double(b.size.height),
                ])
            }
        } catch {
            FileHandle.standardError.write("ocr fail \(f): \(error)\n".data(using: .utf8)!)
        }
    }
    let t = Double(f.dropFirst().split(separator: ".").first ?? "0") ?? 0
    results.append(["t": t, "lines": lines])
    if idx % 50 == 0 {
        FileHandle.standardError.write("\(idx)/\(files.count)\n".data(using: .utf8)!)
    }
}

let data = try! JSONSerialization.data(withJSONObject: results, options: [.prettyPrinted, .sortedKeys])
try! data.write(to: URL(fileURLWithPath: outPath))
print("wrote \(outPath) frames=\(results.count)")
