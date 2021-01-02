import praw
import datetime
import random
from tkscrolledframe import ScrolledFrame
import tkinter as tk

REPLY_MESSAGES = ["Happy cake day /u/{}! 🍰",
                  "Happy Reddit birthday /u/{}!",
                  "Hope you have a nice cake day /u/{}! 🎂",
                  "It's your cake day /u/{}! Congrats! 🎉"]


def authenticate():
    print("Authenticating...")
    lb = tk.Label(text='Authenticating...',
                  fg='#3f0052',
                  bg='#d7d5f7',
                  wraplength=400,
                  master=frame,
                  font="-size 9",
                  anchor="w",
                  justify='left',
                  padx='10',
                  pady='4')
    lb.pack()
    root.update_idletasks()
    root.update()
    reddit = praw.Reddit("Birth-Day-Bot", user_agent="Birthday Bot v1.0")
    return reddit


def hide_all_frames():
    for widget in frame.winfo_children():
        widget.destroy()


def main():
    hide_all_frames()
    reddit = authenticate()
    congratulated_users = get_congratulated_users()

    remove_downvoted_comments(reddit)
    run_bot(reddit, congratulated_users)
    root.mainloop()


def run_bot(reddit, congratulated_users):
    current_date = datetime.datetime.today().strftime('%y/%m/%d')

    print("Getting comments...")
    lb = tk.Label(text='Getting comments...',
                  fg='#3f0052',
                  bg='#d7d5f7',
                  wraplength=400,
                  master=frame,
                  font="-size 9",
                  anchor="w",
                  justify='left',
                  padx='4',
                  pady='4')
    lb.pack()
    root.update_idletasks()
    root.update()
    for comment in reddit.subreddit("RandomKindness+happy").comments(limit=200):

        account_created_date = datetime.datetime.fromtimestamp(int(comment.author.created)).strftime('%y/%m/%d')

        print("Checking...")
        lb = tk.Label(text='Checking...',
                      fg='#3f0052',
                      bg='#d7d5f7',
                      wraplength=400,
                      master=frame,
                      font="-size 9",
                      anchor="w",
                      justify='left',
                      padx='4',
                      pady='4')
        lb.pack()
        root.update_idletasks()
        root.update()
        if current_date != account_created_date \
                and current_date[3:] == account_created_date[3:] \
                and comment.author not in congratulated_users:
            print("Cake day found!")
            lb = tk.Label(text='Cake day found!',
                          fg='#77E6AB',
                          bg='#d7d5f7',
                          wraplength=400,
                          master=frame,
                          font="-size 9",
                          anchor="w",
                          justify='left',
                          padx='4',
                          pady='4')
            lb.pack()
            root.update_idletasks()
            root.update()
            comment.reply(random.choice(REPLY_MESSAGES).format(comment.author)).clear_vote()

            congratulated_users.append(comment.author)
            with open("congratulated_users.txt", "a") as file:
                file.write("{}\n".format(comment.author.name))


def get_congratulated_users():
    with open("congratulated_users.txt", "r") as file:
        return file.read().split("\n")


def remove_downvoted_comments(reddit):
    print("Checking for comments with negative karma...")
    lb = tk.Label(text='Checking for comments with negative karma...',
                  fg='#3f0052',
                  bg='#d7d5f7',
                  wraplength=400,
                  master=frame,
                  font="-size 9",
                  anchor="w",
                  justify='left',
                  padx='10',
                  pady='4')
    lb.pack()
    root.update_idletasks()
    root.update()

    for comment in reddit.redditor("Birth-Day-Bot").comments.new(limit=20):
        print("Comment Score: {}".format(comment.score))
        lb = tk.Label(text='Comment Score: {}'.format(comment.score),
                      fg='#EE7373',
                      bg='#d7d5f7',
                      wraplength=400,
                      master=frame,
                      font="-size 9",
                      anchor="w",
                      justify='left',
                      padx='10',
                      pady='4')
        lb.pack()
        root.update_idletasks()
        root.update()
        if comment.score <= 0:
            print("Deleting comment...")
            lb = tk.Label(text='Deleting comment...',
                          fg='#EE7373',
                          bg='#d7d5f7',
                          wraplength=400,
                          master=frame,
                          font="-size 9",
                          anchor="w",
                          justify='left',
                          padx='10',
                          pady='4')
            lb.pack()
            root.update_idletasks()
            root.update()
            comment.delete()


root = tk.Tk()
root.geometry('470x550+0+0')
root.title('Reddit Birthday Bot')
data_frame = tk.Frame(root)
data_frame.pack(side="left", expand=0, fill="both")

sf = ScrolledFrame(data_frame, width=450, bg='#ffffff')
sf.pack(side="left", expand=1, fill="both")
sf.bind_arrow_keys(root)
sf.bind_scroll_wheel(root)

frame = sf.display_widget(tk.Frame)
frame['bg'] = '#d7d5f7'
frame['bd'] = 15
frame['relief'] = 'sunken'
frame['width'] = 450
frame.pack_propagate(1)

b = tk.Button(master=data_frame, text='Run',
              fg='#8132B6',
              bg='#D0C5D8',
              width=14,
              height=2,
              pady='4',
              padx='4',
              command=main)
b.place(relx=0.8, rely=0.5, anchor='center')

if __name__ == "__main__":
    main()
