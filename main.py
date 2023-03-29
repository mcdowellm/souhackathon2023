from time import sleep
import openai
import webbrowser
openai.api_key = 'YOUR_API_KEY_HERE'

# Create a madlibs first with chatGPT
def generate_response(prompt):
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=prompt,
        max_tokens=2048,
        temperature=0,
    )
    return response.choices[0].text


def find_madlib_format(madlib_text):
    adj_ind_start = madlib_text.find('adjective')
    adj_ind_end = adj_ind_start + len('adjective') - 1
    madlib_form_start = ''
    madlib_form_end = ''
    while adj_ind_start - 1 >= 0 and madlib_text[adj_ind_start - 1] != ' ':
        madlib_form_start =  madlib_text[adj_ind_start - 1] + madlib_form_start 
        adj_ind_start -= 1

    while adj_ind_end + 1 < len(madlib_text) and madlib_text[adj_ind_end + 1] != ' ':
        madlib_form_end = madlib_form_end + madlib_text[adj_ind_end + 1] 
        adj_ind_end += 1

    return madlib_form_start, madlib_form_end

def get_title(madlib):
    prompt = f'Give me a title for this story: {madlib}'
    title = generate_response(prompt)
    return title

def get_story_lines(title, madlib):
    all_lines = []
    title_lines = title.split('\n')
    for line in title_lines:
        if line == '':
            continue
        all_lines.append(line)

    madlib_lines = madlib.split('\n')
    for line in madlib_lines:
        if line == '':
            continue
        all_lines.append(line)

    return all_lines


def create_image_URL(title, madlib):
    URLs = []
    prompt_lines = get_story_lines(title, madlib)

    for line in prompt_lines:
        response = openai.Image.create(
            prompt=line + ' Shakespearean.',
            n=1,
            size="1024x1024"
        )
        URLs.append(response.data[0].url)

    return URLs
    
def create_html_page(line, URL):
    f = open('story.html', 'w')
    html_template = f"""
    <html>
    <head>
    <link rel="stylesheet" href="story.css">
    </head>
    <body>
    <div class="imgHolder">
        <figure>
            <img src="{URL}" width=512 height=512>
            <figcaption>{line}</figcaption>
        </figure>
    </div>
    </body>
    </html>
    """
    f.write(html_template)
    f.close()

def create_html_output(title, madlib, URLs):
    lines = get_story_lines(title, madlib)

    for i in range(len(lines)):
        create_html_page(lines[i], URLs[i])
        webbrowser.open_new('story.html')
        sleep(10)

def create_madlib_story():
    prompt = "Make a Shakespearean madlib"
    madlib = generate_response(prompt)

    print("Welcome to Shakespearean MadLibs by ChatGPT and Dall-e!")
    print("Please enter the desired responses and it will create your own Shakespearean story.")
    madlib_form_start, madlib_form_end = find_madlib_format(madlib)

    while True:
        start_index = madlib.find(madlib_form_start)
        end_index = madlib.find(madlib_form_end)
        if start_index == -1 or end_index == -1:
            break

        word_sub = input(f'Give me a {madlib[(start_index + 1):end_index]}: ')
        madlib = madlib[:(start_index)] + word_sub + madlib[(end_index + 1):]

    print("All done! We are generating your story now!")
    title = get_title(madlib)
    URLs = create_image_URL(title, madlib)
    create_html_output(title, madlib, URLs)


create_madlib_story()




