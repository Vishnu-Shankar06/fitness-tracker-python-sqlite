from database import Database
import json
import os
import random
from datetime import datetime, timedelta

class FitnessTracker:
    def __init__(self,quotes_file="quotes.json"):
        self.db = Database()
        self.quotes_file = quotes_file
        self.name = ""
        self.workout_days = []
        self.rest_days = []
        self.workout_time = ""
        self.daily_streak = 0
        self.weekly_streak = 0
        self.last_workout_date = ""
        self.workout_history = []
        self.quotes = self.load_quotes()

        print("=== 🏋️ Fitness Tracker Console ===")
        self.login()
        self.check_streak_reset()
        
        print(f"\n✨ Motivation: {random.choice(self.quotes)}")
        
        self.main_menu()
        
    def login(self):
        name = input("Enter your name: ").strip()
        user_data = self.db.get_user(name)

        if user_data:
            self.id = user_data[0]
            self.name = user_data[1]
            self.workout_days = user_data[2].split(',') if user_data[2] else []
            self.workout_time = user_data[3]
            self.daily_streak = user_data[4]
            self.weekly_streak = user_data[5]
            self.last_workout_date = user_data[6]

            history_data = self.db.get_user_workouts(self.id)
            self.workout_history = []
            for row in history_data:
                self.workout_history.append({
                    "date": row[0],
                    "workout": row[1],
                    "reps/duration":row[2]
                })
            print(f"Welcome Back, {self.name}")
        else:
            self.name = name
            self.create_profile()

    def load_quotes(self):
        fallbacks = ["Action is the foundational key to all success.", "Don't stop when you're tired. Stop when you're done."]
        if os.path.exists(self.quotes_file):
            try:
                with open(self.quotes_file, "r") as f:
                    return json.load(f).get("quotes", fallbacks)
            except (FileNotFoundError, json.JSONDecodeError):
                return fallbacks
        return fallbacks

    def check_streak_reset(self):
        """Resets streak if the user missed their last scheduled workout day."""
        if not self.last_workout_date:
            return

        today = datetime.now().date()
        last_date = datetime.strptime(self.last_workout_date, "%Y-%m-%d").date()
        
        delta = (today - last_date).days
        if delta > 1:
            streak_broken = False

            for i in range(1, delta):
                missed_date = last_date + timedelta(days=i)
                missed_day_name = missed_date.strftime("%A")
                
                if missed_day_name in self.workout_days:
                    streak_broken = True
                    break 
            
            if streak_broken:
                print("\n⚠️ Streak reset! You missed a scheduled workout. Consistency is key!")
                self.daily_streak = 0
                self.db.update_user_stats(self.id, self.daily_streak, self.weekly_streak, self.last_workout_date)

    def create_profile(self):
        print("\n=== Create Your Profile ===")
        while True:
            try:
                choice = int(input("How many workout days per week? (recommended 3-6, max 7): "))
                if choice < 3 or choice > 7:
                    print("Invalid choice. Please enter a number between 3 and 7.")
                    continue
                if choice == 3:
                    print("Good 3 days is the standard baseline for consistency.")
                elif choice == 4:
                    print("Nice 4 days gives you balance between effort and recovery.")
                elif choice == 5:
                    print("Great 5 days shows strong commitment and steady progress.")
                elif choice == 6:
                    print("Impressive 6 days is ambitious, just be mindful of recovery!")
                elif choice == 7:
                    print("Wow 7 days means no rest! Be careful, recovery is essential.")
                break
            except ValueError:
                print("Please enter a valid number (3-7).")
        
        days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
                      
        if choice == 7:
            print("7 days selected! Automatically setting all days as workout days. ⚡")
            self.workout_days = days.copy()
            self.rest_days = []
        else:
            print("\nSelect your workout days (enter numbers separated by space no commas needed) :")
            for i, day in enumerate(days, 1):
                print(f"{i}:{day}")
            
            while True:
                selections = input("Your Choices (Enter the nums spaced): ").split()
                try:
                    selected_indexes = sorted(list(set(int(item) for item in selections)))
                    if len(selected_indexes) != choice:
                        print(f"Please enter exactly {choice} unique numbers.")
                        continue
                    if all(1 <= idx <= 7 for idx in selected_indexes):
                        break
                    else:
                        print("Choose numbers between 1 and 7.")
                except ValueError:
                    print("Enter valid numbers only.")
                                      
            self.workout_days = [days[idx - 1] for idx in selected_indexes]
            self.rest_days = [day for day in days if day not in self.workout_days]
                                                       
        self.workout_time = input("Enter preferred workout time (e.g., 6 AM):").strip().upper()
        self.daily_streak = 0
        self.weekly_streak = 0
                                                                   
        days_string = ",".join(self.workout_days)  
        self.db.add_user(self.name,days_string,self.workout_time)   
        new_user = self.db.get_user(self.name)   
        self.id = new_user[0]  
                                                                                     
        print("\nProfile created successfully! 💪")
                                             
    def log_today(self):         
        today_name = datetime.now().strftime("%A")                  
        today_date = datetime.now().strftime("%Y-%m-%d")                
                                
        if today_name not in self.workout_days:                      
            print(f"Today is {today_name}, which is a rest day! Rest is progress too.")               
            return         
                                                                              
        if any(w["date"] == today_date for w in self.workout_history):        
            print("✅ You've already logged today's workout!")          
            return                                                           
                                                             
        print(f"\n--- Logging for {today_name} ---")                           
        workout = input("Workout name (or type 'Push'/'Pull'/'Legs'): ")                    
        reps = input("Duration/Sets: ")                        
                                                                     
        self.workout_history.append({             
            "date": today_date,  
            "day": today_name,  
            "workout": workout,  
            "reps/duration": reps  
        })   
                                                  
        self.daily_streak += 1                
        self.last_workout_date = today_date   
        
        current_year, current_week, _ = datetime.now().isocalendar()
        completed_this_week = 0
        for w in self.workout_history:
            w_year, w_week, _ = datetime.strptime(w["date"], "%Y-%m-%d").isocalendar()
            if w_year == current_year and w_week == current_week:
                completed_this_week += 1
                
        if completed_this_week == len(self.workout_days):
            self.weekly_streak += 1
            print(f"🎉 WEEKLY GOAL MET! Weekly Streak is now {self.weekly_streak}!")
                     
        self.db.log_workout(self.id,today_date,workout,reps)                                          
        self.db.update_user_stats(self.id,self.daily_streak,self.weekly_streak,self.last_workout_date)              
                                                                                     
        print(f"🔥 Awesome! {workout} logged. Current streak: {self.daily_streak}")                  
                                                                               
    def show_stats(self):                                   
        print("\n" + "="*25) 
        print(f"STATISTICS FOR {self.name.upper()}")      
        print(f"Current Streak: {self.daily_streak} Days")   
        print(f"Weekly Streak: {self.weekly_streak} Weeks")
        print(f"Total Workouts: {len(self.workout_history)}")   
                                                                     
        current_year, current_week, _ = datetime.now().isocalendar()        
            
        completed_this_week = 0 
        for w in self.workout_history: 
            w_year, w_week, _ = datetime.strptime(w["date"], "%Y-%m-%d").isocalendar() 
            if w_year == current_year and w_week == current_week:  
                completed_this_week += 1  
                        
        goal = len(self.workout_days)                             
        percent = (completed_this_week / goal) * 100 if goal > 0 else 0      
        bar = "█" * int(percent / 10) + "-" * (10 - int(percent / 10))             
        
        print(f"Weekly Goal:   |{bar}| {percent:.0f}% ({completed_this_week}/{goal})")      
        print("="*25)     
        
        if input("\nView history? (y/n): ").lower() == 'y': 
            for w in self.workout_history[:]:  
                print(f"• {w['date']}: {w['workout']} - {w['reps/duration']}")

    def reminder(self):
        current_time = datetime.now().strftime("%I %p").lstrip("0").upper()
        if current_time.replace(" ", "") == self.workout_time.replace(" ", ""):
            print("\n🔔 NOTIFICATION: It's workout time! Get moving!")

    def main_menu(self):
        while True:
            self.reminder()
            print("\n1. 🏋️ Log Workout")
            print("2. 📊 View Stats")
            print("3. ⚙️ Update Schedule")
            print("4. 🚪 Exit")

            choice = input("\nAction: ")

            if choice == "1":
                self.log_today()
            elif choice == "2":
                self.show_stats()
            elif choice == "3":
                self.create_profile()
            elif choice == "4":
                print(f"Keep it up, {self.name}. See you next time!")
                print(f"✨ Parting Motivation: {random.choice(self.quotes)}")
                break
            else:
                print("Invalid choice.")

if __name__ == "__main__":
    FitnessTracker()