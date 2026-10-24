import Foundation
import CoreText
import CoreGraphics
let font=CTFontCreateWithName("AvenirNext-DemiBold" as CFString,1000,nil)
let chars=Array("STRATUS".utf16)
var glyphs=[CGGlyph](repeating:0,count:chars.count)
guard CTFontGetGlyphsForCharacters(font,chars,&glyphs,chars.count) else {fatalError("Missing wordmark glyph")}
var advances=[CGSize](repeating:.zero,count:glyphs.count)
CTFontGetAdvancesForGlyphs(font,.horizontal,glyphs,&advances,glyphs.count)
var paths=[String](),x:CGFloat=20,bounds=CGRect.null
func f(_ x:CGFloat)->String {String(format:"%.2f",Double(x))}
for (i,glyph) in glyphs.enumerated(){
 guard let path=CTFontCreatePathForGlyph(font,glyph,nil) else {fatalError("Missing outline")}
 var transform=CGAffineTransform(translationX:x,y:0)
 guard let positioned=path.copy(using:&transform) else {fatalError("Outline transform failed")}
 bounds=bounds.union(positioned.boundingBoxOfPath)
 var d=""
 positioned.applyWithBlock { pointer in
  let e=pointer.pointee,p=e.points
  switch e.type {
  case .moveToPoint:d += "M\(f(p[0].x)),\(f(p[0].y))"
  case .addLineToPoint:d += "L\(f(p[0].x)),\(f(p[0].y))"
  case .addQuadCurveToPoint:d += "Q\(f(p[0].x)),\(f(p[0].y)) \(f(p[1].x)),\(f(p[1].y))"
  case .addCurveToPoint:d += "C\(f(p[0].x)),\(f(p[0].y)) \(f(p[1].x)),\(f(p[1].y)) \(f(p[2].x)),\(f(p[2].y))"
  case .closeSubpath:d += "Z"
  @unknown default:break
  }
 }
 paths.append(d);x += advances[i].width+44
}
let width=bounds.maxX+20,height=bounds.height+30,baseline=bounds.maxY+15
let svg="""
<svg xmlns="http://www.w3.org/2000/svg" width="\(f(width))" height="\(f(height))" viewBox="0 0 \(f(width)) \(f(height))"><title>STRATUS</title><defs><linearGradient id="front" x1="0" y1="0" x2=".25" y2="1"><stop stop-color="#f0fff4"/><stop offset=".42" stop-color="#cde7d5"/><stop offset="1" stop-color="#90baa1"/></linearGradient></defs><g transform="translate(0 \(f(baseline))) scale(1 -1)" fill="url(#front)" stroke="#e3ffec" stroke-width="1.4">\(paths.map {"<path d=\"\($0)\"/>"}.joined())</g></svg>
"""
try svg.write(toFile:CommandLine.arguments[1],atomically:true,encoding:.utf8)
print("Created seven outlined letters: STRATUS. Aspect ratio \(f(width/height)).")
