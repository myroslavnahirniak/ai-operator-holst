# 30.09: картинка для блока AI-таргет в холсте (вместо робота), 2 варианта, Higgsfield GPT Image 2.5
import json, re, subprocess, sys, concurrent.futures as cf
STYLE = ("Wide cinematic photoreal 3D render in exactly the visual style of the reference images: pure near-black background, "
         "matte black objects, soft warm volumetric light, electric-yellow (#FDD506) glowing accents, premium minimal keynote look, lots of empty dark space, shallow depth of field. "
         "Absolutely no readable text, no letters, no numbers, no logos, no watermark, no people, no robots. ")
P = {
 'a': "Scene: an AI advertising agent at work, shown only as a small glowing golden core floating above a sleek matte-black desk. "
      "In front of it hovers a row of five square social-media ad cards (abstract image thumbnails only). Thin golden light streams flow from the core into the two best cards, "
      "which glow bright yellow with small rising golden bar charts above them; the middle card is neutral; the two cards on the right are dimmed dark grey with a tiny pause symbol, switched off. "
      "The feeling: budget is moved every day to where leads are cheaper, and what wastes money is turned off.",
 'b': "Scene: a minimalist matte-black control console seen from a low angle. On it stand small glass tiles like ad creatives on thin stands, arranged in a gentle arc. "
      "Golden coins of light slide along a thin glowing track from the dim tiles on the left toward two bright yellow glowing tiles on the right, which have small rising light bars behind them. "
      "The dim tiles are dark and switched off. Represents an AI agent automatically moving ad budget to the winning ads, 24/7, calm and precise.",
}
def run(k):
    cmd = ['higgsfield','generate','create','gpt_image_2_5','--prompt',STYLE+P[k],'--aspect_ratio','16:9','--resolution','2k','--quality','high',
           '--image-references','ref-robot.png','--image-references','ref-answer.png','--wait','--wait-timeout','20m','--json']
    p = subprocess.run(cmd, capture_output=True, text=True)
    m = re.search(r'https://[^"\s]+\.(?:png|jpg|jpeg|webp)', p.stdout)
    if not m: return k, 'FAIL ' + (p.stdout + p.stderr)[-300:]
    subprocess.run(['curl','-4','-sS','-L','-m','180','--retry','3','-o',f'ads-{k}.png',m.group(0)])
    return k, 'ok'
with cf.ThreadPoolExecutor(2) as ex:
    for k, r in ex.map(run, sorted(P)): print(k, r, flush=True)
