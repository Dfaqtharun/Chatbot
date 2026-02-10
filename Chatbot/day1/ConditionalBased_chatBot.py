user = input("you:").lower()
bot =""
if user =="hi":
    bot ="hello"
elif user =="hello":
    bot ="how may i assit you"
elif user =="name":
    bot = "I am simple chatBot"
elif user =="bye":
    bot="good bye have a good Day"
else :
    bot ="i dont understand"
print("Bot: ",bot)