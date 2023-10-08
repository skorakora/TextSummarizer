import urwid
import subprocess
from os import system, name
import g4f

action = 'none'
model = 'none'



actions = [
    u'Summarize text in 3 sentences',
    u'Summarize text in 1 paragraph',
    u'Summarize text in 2 paragraphs',
    u'Summarize text in 5 paragraphs',
    u'Explain text in simple words and simplify in 3 sentences',
    u'Explain text in simple words and simplify in 1 paragraph',
    u'Explain text in simple words and simplify in 2 paragraphs',
    u'Explain text in simple words and simplify in 5 paragraphs'
    ]

models = [
    u'GPT3.5',
    u'GPT4'
    ]

titles = [u'Choose action',u'Choose model']






#get text from clipboard
def get_selected_text_clipboard():
    try:
        # Use xclip to get the selected text from the clipboard
        selected_text = subprocess.check_output(["xclip", "-o", "-selection", "primary"], universal_newlines=True)
        return selected_text
    except subprocess.CalledProcessError:
        return None


textRegister = get_selected_text_clipboard() #contains clipboard text


#returns first five words of string if it is longer than five words
def get_first_five_words(text):
    words = text.split()
    if len(words) <= 5:
        return " ".join(words)
    else:
        return " ".join(words[:5]) + " ..."

#creates a selection menu and returns selected item
class SelectionMenu:

    #clears the menu
    def Clear(self):
        system('clear')

    def GetSelection(self):
        return self.selection



    def menu(self,title, selections):
        body = [urwid.Text(title), urwid.Divider()]
        for c in selections:
            button = urwid.Button(c)
            body.append(urwid.AttrMap(button, None, focus_map='reversed'))

        body.append(urwid.Text(('banner', u"======================================="), align='center'))
        body.append(urwid.Text(('banner', u" choosen text "), align='center'))
        body.append(urwid.Text(('banner', get_first_five_words(textRegister)), align='center'))
        return urwid.ListBox(urwid.SimpleFocusListWalker(body))


    def __init__(self, title, selections):
        self.title = title
        self.selections = selections
        self.selection = 'none'
        self.main = urwid.Padding(self.menu(self.title,self.selections), left=2, right=2)
        top = urwid.Overlay(self.main, urwid.SolidFill(u'\N{MEDIUM SHADE}'),
            align='center', width=('relative', 60),
            valign='middle', height=('relative', 60),
            min_width=20, min_height=9)
        urwid.MainLoop(top, palette=[('reversed', 'standout', '')],unhandled_input=self.key_handler).run()

    def key_handler(self,key):

        if key == 'enter' or key == 'meta w':
            self.selection = self.selections[self.main.original_widget.focus_position-2]
            raise urwid.ExitMainLoop()
            return



        if self.main.original_widget.focus_position == 2:
            if key[0] == 'mouse press' and key[1] == 4:
                return
            elif key[0] == 'mouse press' and key[1] == 5:
                self.main.original_widget.focus_position += 1
                return

        if self.main.original_widget.focus_position == len(self.selections) + 1:
            if key[0] == 'mouse press' and key[1] == 4:
                self.main.original_widget.focus_position -= 1
                return
            elif key[0] == 'mouse press' and key[1] == 5:
                return

        if key[0] == 'mouse press' and key[1] == 4:
            self.main.original_widget.focus_position -= 1
        elif key[0] == 'mouse press' and key[1] == 5:
            self.main.original_widget.focus_position += 1


def GetResponse(prompt,model):

    '''

    Supported models by g4f, but not implemented -> todo implement all models in the future

    h2ogpt-gm-oasst1-en-2048-falcon-7b-v3
    h2ogpt-gm-oasst1-en-2048-falcon-40b-v1
    h2ogpt-gm-oasst1-en-2048-open-llama-13b
    claude-instant-v1
    claude-v1
    claude-v2
    command-light-nightly
    command-nightly
    gpt-neox-20b
    oasst-sft-1-pythia-12b
    oasst-sft-4-pythia-12b-epoch-3.5
    santacoder
    bloom
    flan-t5-xxl
    code-davinci-002
    gpt-3.5-turbo-16k
    gpt-3.5-turbo-16k-0613
    gpt-4-0613
    text-ada-001
    text-babbage-001
    text-curie-001
    text-davinci-002
    text-davinci-003
    llama13b-v2-chat
    llama7b-v2-chat
    '''



    match model:
        case 'GPT3.5':
            response = g4f.ChatCompletion.create(model="gpt-3.5-turbo",messages=[{"role": "user", "content": prompt}],stream=True,)
        case 'GPT4':
            response = g4f.ChatCompletion.create(model="gpt-4",messages=[{"role": "user", "content": prompt}],stream=True,)
        case 'LLama':
            response = g4f.ChatCompletion.create(model="llama13b-v2-chat",messages=[{"role": "user", "content": prompt}],stream=True,)


    concatenated_message = ""

    for message in response:
        concatenated_message = concatenated_message + message

    return concatenated_message








#===============================PROGRAM STARTS HERE=====================================



actionMenu = SelectionMenu(titles[0],actions)

action = actionMenu.GetSelection()

actionMenu.Clear()


modelMenu = SelectionMenu(titles[1],models)

model = modelMenu.GetSelection()

modelMenu.Clear()

prompt = action + ': ' + textRegister

system('clear')

print('=================================================')
print('Waiting for API response, please wait, it will take a few seconds...')
print('=================================================')

response = GetResponse(prompt,model)

system('clear')


def keyboard_handler(key):
    if key == 'meta e':
        raise urwid.ExitMainLoop()


text = urwid.Text(response + '\n=================================================\nPress alt+e to exit\n=================================================\n')


fill = urwid.Filler(text, 'top')


loop = urwid.MainLoop(fill,unhandled_input=keyboard_handler).run()

exit()












