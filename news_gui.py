import io
import webbrowser
import requests
from tkinter import *
from urllib.request import urlopen
from PIL import ImageTk, Image
import urllib.request
from urllib.error import HTTPError



class NewsApp:
    def __init__(self):
        # fetch data
        self.data = requests.get(
            'https://newsapi.org/v2/top-headlines?country=in&apiKey=2de1e478f59d48b88027b2bdbbd792c7').json()

        # initial GUI load
        self.load_gui()

        # load the 1'st news item
        self.load_news_item(2)

    def load_gui(self):
        self.root = Tk()
        self.root.geometry('350x600')
        self.root.resizable(0, 0)  # so that the gui size dont change
        self.root.configure(background='black')

    def clear(self):
        for i in self.root.pack_slaves():
            i.destroy()

    def open_link(self, url):
        webbrowser.open_new_tab(url)

    def load_news_item(self, index):  # firstly clear screen for new news item

        self.clear()

        try:
            img_url = self.data['articles'][index].get('urlToImage',
                                                       '')  # Get the image URL or an empty string if it's None
            if img_url:  # Check if the image URL is not empty
                # Create a Request object with a timeout value
                req = urllib.request.Request(img_url, headers={'User-Agent': 'Mozilla/5.0'})
                response = urlopen(req, timeout=10)
                raw_data = response.read()

                im = Image.open(io.BytesIO(raw_data)).resize((350, 250))
                photo = ImageTk.PhotoImage(im)

                label = Label(self.root, image=photo)
                label.pack()
            else:
                # Display a placeholder image if the image URL is null or empty
                placeholder_image = Image.open("placeholder.jpg").resize((350, 250))
                photo = ImageTk.PhotoImage(placeholder_image)
                label = Label(self.root, image=photo)
                label.pack()

        except HTTPError as e:
            # Handle HTTP errors gracefully
            print(f"Error fetching image: {e}")
            # Provide a fallback image or default image
            placeholder_image = Image.open("placeholder.jpg").resize((350, 250))
            photo = ImageTk.PhotoImage(placeholder_image)
            label = Label(self.root, image=photo)
            label.pack()

        heading = Label(self.root, text=self.data['articles'][index]['title'], bg='black', fg='white', wraplength=350,
                        justify='center')
        heading.pack(pady=(10, 20))
        heading.config(font=('verdana', 15))

        description = self.data['articles'][index].get('description','')  # Get the description or an empty string if it's None

        details = Label(self.root, text=description, bg='black', fg='white',
                        wraplength=350, justify='center')
        details.pack(pady=(2, 20))
        details.config(font=('verdana', 12))

        # buttons --------------------------------------------------------------------------------------------
        frame = Frame(self.root, bg='black')  # for making buttons
        frame.pack(side=BOTTOM, fill=X)  # Set the side to BOTTOM and fill to X to align with the bottom of the window

        if index != 0:
            prev = Button(frame, text='Prev', width=16, height=3, command=lambda: self.load_news_item(index - 1))
            prev.pack(side=LEFT)

        read = Button(frame, text='Read More ..', width=16, height=3,
                      command=lambda: self.open_link(self.data['articles'][index]['url']))
        read.pack(side=LEFT)

        if index != len(self.data['articles'])-1:
            next = Button(frame, text='Next', width=16, height=3, command=lambda: self.load_news_item(index + 1))
            next.pack(side=LEFT)

        self.root.mainloop()


obj = NewsApp()
