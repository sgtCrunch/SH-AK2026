import os
import smtplib
from flask import Flask, render_template, request, jsonify, redirect
from werkzeug.utils import secure_filename
from werkzeug.middleware.proxy_fix import ProxyFix
from email.mime.text import MIMEText


app = Flask(__name__)


# ── Config ────────────────────────────────────────────────
UPLOAD_FOLDER   = os.path.join(os.path.dirname(__file__), 'static', 'uploads')
CLUE_FOLDER   = os.path.join(os.path.dirname(__file__), 'static', 'clue-imgs')

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16 MB

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Email configuration
SENDER_EMAIL = os.environ['SENDER_EMAIL']
SENDER_PASSWORD = os.environ['SENDER_PASSWORD']
RECEIVER_EMAIL = os.environ['RECEIVER_EMAIL']
SMTP_SERVER = os.environ['SMTP_SERVER']
SMTP_PORT = int(os.environ['SMTP_PORT'])

def send_email():
    msg = MIMEText("Someone accessed the peace-clue page.")
    msg['Subject'] = 'Peace Clue Accessed'
    msg['From'] = SENDER_EMAIL
    msg['To'] = RECEIVER_EMAIL
    try:
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(SENDER_EMAIL, SENDER_PASSWORD)
        server.sendmail(SENDER_EMAIL, RECEIVER_EMAIL, msg.as_string())
        server.quit()
        print("Email sent successfully")
    except Exception as e:
        print(f"Email failed: {e}")

# ── Sample data — replace with your own source ────────────
Clues = {
    "weird-clue":'''Its fun to remember times when 
                    we were weirder with tons of whimsy. 
                    To be fair you still have plent of both.
                    For this challenge, buy a bouquet of flowers 
                    and pose with the "Lady With Flowers". 
                    In the photo you must imitate Anushe's 
                    favorite Mario character,
                    Waluigi! You know the pose I'm talking about! Make sure
                    you upload the photo on the next page!''',
    "end-clue":'''Happy Birthday Anushe!''',
    "eyebrow-clue":'''Huh, you looking at me? Remember, its a momentous occasion, 
                      don't forget why we are here. You know even Caesar would agree. You haven't 
                      met him? Ask your namesake, he defintely knows him. For the challenge,
                      decypher this: "ilqg brxu idyrulwh errn dqg wdnh d skrwr dv d jurxs."
                      Don't be afraid to use techology!''',
    "avo-clue": '''Phew that was fun! Being 
                    one with nature is important. For this challenge, 
                    take a photo with the view!
                    ''',
    "peace-clue":'''Happy Birthday, Anushe! 

I hope you liked your adventure. It took time and effort, but it's nothing compared to what you provide as a friend. Anushe, you are a remarkable person. You are smart, silly and serious all at the same time, and sometimes when you are garnering all the attention in a room by just being yourself, we all can't help but feel incredibly lucky.

We don't say this often, and to be fair we should. We all care about you immensely, Anushe. We are not talking about a kind of care that dulls over time. It is our deepest hope you realize you will never be truly alone. That when you feel lost or unsure who to lean on, that you, without hesitation, will think of us. Forget all the thoughts that invade your head, telling you it's too much to ask. We will always, enthusiastically, without any second thought, be there for you.

We know your life will be full of adventure, wonder, and love. This was our humble and inspired attempt to give you a small taste of that today.

With much love, 

Your Friends''',
    "paint-clue":'''Pretty cool huh? It challenges our perception of reality
                    and makes us pay attention. For this challenge, you will solve the
                    Anushe themed crossword! Once done take a picture and submit it on the next page.''',
    "baby-clue":'''I hope you enjoyed your mosaic class! 
                We know how much you like making things 
                and we all thought this was perfect.
                For each blue letter clue, you'll 
                find a task to complete and a picture 
                to take and upload. For this one, we would 
                love a group photo of all of you 
                holding up your completed mosaics!
                Go to the last page to upload your photo.
                Make sure to take it first with your phone and
                then click upload to choose it from your library.''',
    "puzzclue":'''Whoa! Not gonna lie I thought you weren't 
                    gonna find it. You are really good at puzzles! 
                    For this challenge, just pose with your finished puzzle, 
                    make sure you are smoking your invisible cigar! 
                    Upload the photo on the next page!'''
}

travel_clues = {
    "weird-clue":'''Beautiful poses! Truly breathtaking! 
                    To find your next location, you must seek 
                    the Scottish soldier 
                    hes always on the Lookout. 
                    Once there don't pass the Butter?''',
    "eyebrow-clue":'''Dang I should really read more books. 
                      For your next location, we will explore space
                      and light. It is important to examine what is
                      Within and what we are Without. When you do this 
                      and dare to go into the pyramid, you will find your next clue.''',
    "avo-clue":'''I feel zen, don't you? Your next location,
                  is about finding peace with people around the world 
                  and espeically your sister! Did you know that there's a bird
                  that migrates from Japan every year to Canberra? Incredible. One
                  more thing, check the tables when you get there...''',
    "peace-clue":'''Are you hungry? I know I am. For your next location, its dinner time!
                    We have reservation at KOTO Japanese Restaurant for 6:15pm! Don't be late!
                    MMM I love sushi.''',    
    "paint-clue":'''Dang I wish I was that fast. Anushe always beats me badly at those.
                    Anyway, you know whats fun? Tiny little cars made for children going 
                    at unatural speeds. For your next location, find your nearest go-kart race track!''',
    "baby-clue":'''Great job on the mosaics! To find your next location you must
                   find the whimsical and naive Lady With Flowers. She is patiently waiting for her tram
                   to arrive. Go say hi and ask for your next clue!
                ''',
    "puzzclue":'''Dang really speeding through this. 
                  For your next location, you need to seek the stacks.
                  They say knowledge is power so go find YY 358.24 K12, I guess its 
                  in your namesake? Also don't go too far, this is almost over.'''
}


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def clean_text(text):
    """Remove newlines and tabs from text, preserving single spaces."""
    return ' '.join(text.split())


# ── Routes ────────────────────────────────────────────────
# This route handles the root URL, e.g., "/"
# @app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def letter(path):
    print(f"Received request for path: {path}")
    
    # Check if path exists in Clues to prevent KeyError from malicious requests
    if path not in Clues:
        from flask import abort
        abort(404)
    
    clue_img_url = f'/static/clue-imgs/{path}.jpg'

    if(path == 'peace-clue'):
        send_email()
        cleaned_text = Clues[path]
    else:
        cleaned_text = clean_text(Clues[path])

    pages = [[clue_img_url, cleaned_text]]

    return render_template('blue-letter.html', 
                           pages=pages,
                           background_url=f'/static/backgrounds/{path}.png',
                           song_url=f'/static/clue-songs/{path}.mp3', 
                           redirect_url=f'/{path}/completed')

@app.route('/<path:path>/completed')
def note(path):
    # Check if path exists in travel_clues to prevent KeyError
    if path not in travel_clues:
        from flask import abort
        abort(404)
    
    travel_clue = travel_clues[path]

    return render_template('travel-clue.html',
                           background_url=f'/static/backgrounds/travel-clue.gif', 
                           clue=clean_text(travel_clue))


@app.route('/robots.txt')
def robots():
    return app.send_static_file('robots.txt')


@app.route('/uploads/admin')
def show_uploads():
    upload_dir = os.path.join(os.path.dirname(__file__), 'static', 'uploads')
    if not os.path.isdir(upload_dir):
        image_files = []
    else:
        image_files = [f for f in os.listdir(upload_dir)
                       if os.path.isfile(os.path.join(upload_dir, f))
                       and f.lower().rsplit('.', 1)[-1] in ALLOWED_EXTENSIONS]

    # sort by newest first
    image_files.sort(key=lambda f: os.path.getmtime(os.path.join(upload_dir, f)), reverse=True)

    image_urls = [f"/static/uploads/{f}" for f in image_files]
    return render_template('show-uploads.html', images=image_urls)


@app.route('/upload-photo', methods=['POST'])
def upload_photo():
    if 'photo' not in request.files:
        return jsonify({'error': 'No file part'}), 400

    file = request.files['photo']

    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    if file and allowed_file(file.filename):
        # Get the endpoint that sent the request from the referrer
        from urllib.parse import urlparse
        base, ext = os.path.splitext(file.filename)
        
        if request.referrer:
            parsed_url = urlparse(request.referrer)
            origin_endpoint = parsed_url.path.strip('/') or 'index'
        else:
            origin_endpoint = 'upload'
        
        filename  = f'{origin_endpoint}{ext}'
        save_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)

        file.save(save_path)
        url = f'/static/uploads/{filename}'
        return jsonify({'url': url, 'filename': filename})

    return jsonify({'error': 'File type not allowed'}), 400


if __name__ == '__main__':
    app.run(debug=True)
