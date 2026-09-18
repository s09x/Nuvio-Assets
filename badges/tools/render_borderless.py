"""Render the approved borderless collection using Pillow and an external font."""
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
from collections import Counter
import argparse
import hashlib
import json
import math
import shutil
from PIL import Image, ImageDraw, ImageFont, ImageStat, ImageMath


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load(path):
    return json.loads(path.read_text(encoding="utf-8"))


def dump(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2)+"\n", encoding="utf-8")


def ink(image):
    image = image.convert("RGBA")
    bounds = image.getchannel("A").getbbox()
    assert bounds, "Empty artwork"
    return image.crop(bounds)


def text_art(label, font_path, color="#F3F4F6"):
    selected = ImageFont.truetype(str(font_path), 1600)
    bounds = selected.getbbox(label)
    scale = min(1, 3500/(bounds[2]-bounds[0]), 1740/(bounds[3]-bounds[1]))
    selected = ImageFont.truetype(str(font_path), math.floor(1600*scale))
    bounds = selected.getbbox(label)
    image = Image.new("RGBA", (bounds[2]-bounds[0]+16, bounds[3]-bounds[1]+16))
    ImageDraw.Draw(image).text((8-bounds[0], 8-bounds[1]), label, font=selected, fill=color, stroke_width=0)
    return ink(image)


def centered_code(flag, lettering, color):
    lettering = ink(lettering)
    sx = .5 if (flag.width-lettering.width) % 2 else 0
    sy = .5 if (flag.height-lettering.height) % 2 else 0
    if sx or sy:
        size = (lettering.width+bool(sx), lettering.height+bool(sy))
        alpha = lettering.getchannel("A")
        # A symmetric half-pixel filter preserves both antialiased support edges.
        # Ceil quantization keeps a source edge with alpha=1 from disappearing.
        for axis,shift in enumerate((sx,sy)):
            if shift:
                extent=(alpha.width+(axis==0),alpha.height+(axis==1))
                first=Image.new("L",extent);second=Image.new("L",extent)
                first.paste(alpha,(0,0));second.paste(alpha,(int(axis==0),int(axis==1)))
                alpha=ImageMath.lambda_eval(lambda x:(x['a']+x['b']+1)/2,a=first.convert('I'),b=second.convert('I')).convert('L')
        lettering = Image.new("RGBA", size, color)
        lettering.putalpha(alpha)
    x, y = (flag.width-lettering.width)//2, (flag.height-lettering.height)//2
    b = lettering.getchannel("A").getbbox()
    margins = [x+b[0], flag.width-x-b[2], y+b[1], flag.height-y-b[3]]
    assert margins[0] == margins[1] and margins[2] == margins[3], margins
    flag.alpha_composite(lettering, (x,y))
    return {"field_size":list(flag.size), "visible_letter_bounds":[x+b[0],y+b[1],x+b[2],y+b[3]],
        "margins_left_right_top_bottom_px":margins, "horizontal_center_error_px":0, "vertical_center_error_px":0}


def encode(image, path):
    path.parent.mkdir(parents=True, exist_ok=True)
    image.save(path, format="WEBP", lossless=True, exact=True, method=1)
    with Image.open(path) as decoded:
        assert decoded.convert("RGBA").tobytes() == image.tobytes(), path


def save_art(image, master, web, flag=False):
    image = ink(image)
    image.thumbnail((3520,1840),Image.Resampling.LANCZOS)
    canvas = Image.new("RGBA",(3840,2160))
    canvas.alpha_composite(image,((3840-image.width)//2,(2160-image.height)//2))
    encode(canvas,master)
    save_web(image,web,flag)


def save_web(image, web, flag=False):
    image=ink(image)
    if not flag:
        px,py=math.ceil(image.height*3/13),math.ceil(image.height*1.5/13)
        padded=Image.new("RGBA",(image.width+2*px,image.height+2*py))
        padded.alpha_composite(image,(px,py))
        image=padded
    image.thumbnail((900,600),Image.Resampling.LANCZOS)
    encode(image,web)


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root",type=Path,default=Path(__file__).resolve().parents[1])
    parser.add_argument("--font",type=Path,required=True)
    parser.add_argument("--workers",type=int,default=3)
    parser.add_argument("--only-kind",choices=["flat-language-flag"],help="Refresh one artwork class after an input correction")
    args=parser.parse_args()
    root=args.root.resolve()
    plan=load(root/"data/borderless-render-plan.json")
    assert sha(args.font)==plan["font_sha256"], "Use the approved typeface"
    catalog=load(root/"data/catalog.json")
    lookup={i["id"]:i for i in catalog["items"]}
    results={}
    if args.only_kind:
        previous=load(root/"data/borderless-render-results.json")
        results={i["id"]:i for i in previous["items"]}

    def render(job):
        item=lookup[job["id"]]
        master,web=root/item["master"],root/item["web"]
        kind=job["kind"]
        alignment=job.get("alignment")
        if "seed_master" in job:
            source=root/job["seed_master"]
            assert sha(source)==job["seed_master_sha256"]
            if source.suffix==".webp":shutil.copyfile(source,master)
            else:encode(Image.open(source).convert("RGBA"),master)
            source=root/job["seed_web"]
            assert sha(source)==job["seed_web_sha256"]
            shutil.copyfile(source,web)
        elif kind=="original-logo" and "image" not in job:
            # Existing original masters are immutable rendering inputs.
            assert sha(master)==job["preserved_master_sha256"]
            save_web(Image.open(master).convert("RGBA"),web)
        elif kind=="original-logo":
            original=root/job["image"]
            assert sha(original)==job["image_sha256"]
            image=ink(Image.open(original))
            scale=min(3520/image.width,1840/image.height)
            image=image.resize((round(image.width*scale),round(image.height*scale)),Image.Resampling.LANCZOS)
            save_art(image,master,web)
        elif kind=="flat-language-flag":
            source=root/job["field"]
            assert sha(source)==job["field_sha256"]
            flag=Image.open(source).convert("RGBA")
            assert flag.size==(3200,1600)
            color=job["text_color"]
            text=text_art(job["label"],args.font,color)
            text.thumbnail((1860,896),Image.Resampling.LANCZOS)
            alignment=centered_code(flag,text,color)
            save_art(flag,master,web,True)
        else:
            assert kind=="neutral-text"
            save_art(text_art(job["label"],args.font),master,web)
        with Image.open(master) as decoded:
            decoded.load()
            assert decoded.size==(3840,2160) and decoded.mode=="RGBA"
            assert decoded.getchannel("A").getextrema()==(0,255)
        with Image.open(web) as decoded:
            decoded.load()
            web_size=list(decoded.size)
        return {"id":job["id"],"kind":kind,"sha256":sha(master),"web_sha256":sha(web),"web_size":web_size,
            "bytes":master.stat().st_size,"alignment":alignment,"added_frame":False,"added_shadow":False,
            "added_material_effects":False,"lossless_output_verified":True}

    all_primary=[j for j in plan["items"] if "alias_of" not in j]
    primary=[j for j in all_primary if not args.only_kind or j["kind"]==args.only_kind]
    with ThreadPoolExecutor(max_workers=args.workers) as pool:
        for count,result in enumerate(pool.map(render,primary),1):
            results[result["id"]]=result
            if count%50==0:print(json.dumps({"rendered":count,"unique_total":len(primary)}),flush=True)
    for job in plan["items"]:
        if "alias_of" in job:
            source=lookup[job["alias_of"]]
            target=lookup[job["id"]]
            for key in ("master","web"):shutil.copyfile(root/source[key],root/target[key])
            results[job["id"]]={**results[job["alias_of"]],"id":job["id"],"alias_of":job["alias_of"]}
    obsolete=("tier","material","render_signature","cap_height_px","geometry_sha256","components","composition",
        "background","flag_background","source_type","source_dimensions","flag_verification")
    for job in plan["items"]:
        item=lookup[job["id"]]
        for key in obsolete:item.pop(key,None)
        item.update(results[job["id"]])
        item.update({"label":job["label"],"name":job.get("name",item["name"]),"status":"approved-for-publication",
            "width":3840,"height":2160,"recommended_background":job.get("recommended_background","dark"),
            "provenance":job["provenance"],"design_revision":"2.0.0"})
        if job["kind"]=="flat-language-flag":item["flag_country_code"]=job["country_code"]
    assert len(results)==1037
    for key in ("approved_geometry_sha256","statistics","language_flag_revision"):catalog.pop(key,None)
    catalog.update({"version":"2.0.0","status":"approved-for-publication","approval_scope":
        "User approved original logos plus neutral borderless typography, centered flat flags, and the HDR10 derivative; publication approved.",
        "design":{"added_frames":False,"added_shadows":False,"added_material_effects":False,"font_sha256":plan["font_sha256"],
            "font":"JetBrains Sans SemiBold","font_software_redistributed":False,"display_aliases":{"2160p":"4K"}}})
    counts=Counter(i["kind"] for i in catalog["items"])
    catalog["statistics"]={"catalog_assets":len(results),"kinds":dict(counts),"categories":dict(Counter(i["category"] for i in catalog["items"]))}
    dump(root/"data/catalog.json",catalog)
    dump(root/"data/borderless-render-results.json",{"version":"2.0.0","status":"passed","unique_renders":len(all_primary),"assets":len(results),"items":list(results.values())})
    print(json.dumps(catalog["statistics"]),flush=True)


if __name__=="__main__":main()
