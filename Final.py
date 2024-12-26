class Application:
    def __init__(self, name, job_id, resume_link, skills, experience, status='Submitted'):
        self.name = name
        self.job_id = job_id
        self.resume_link = resume_link
        self.skills = skills
        self.experience = experience
        self.status = status

    def __str__(self):
        return f"{self.name} - {self.job_id} - {self.status} - Skills: {', '.join(self.skills)} - Experience: {self.experience} years"


class ApplicationManagementSystem:
    def __init__(self):
        self.applications = []  # Task 1 - List to store applications
        self.application_queue = []  # Task 2 - Queue for review
        self.recent_activity_stack = []  # Task 3 - Stack for shortlisting/rejecting
        self.application_tracking = {}  # Task 5 - Linked list equivalent for tracking

    # Task 1 - Submission and Storage
    def submit_application(self):
        name = input("Enter applicant name: ")
        job_id = input("Enter job ID: ")
        resume_link = input("Enter resume link: ")
        skills = input("Enter skills (comma-separated): ").split(',')
        experience = int(input("Enter years of experience: "))
        app = Application(name, job_id, resume_link, skills, experience)
        self.applications.append(app)
        self.application_queue.append(app)
        self.application_tracking[app.name] = ["Submitted"]
        print(f"Application submitted for {name}")

    # Task 2 - Process applications (FIFO)
    def process_application(self):
        if self.application_queue:
            app = self.application_queue.pop(0)
            app.status = 'Under Review'
            self.application_tracking[app.name].append('Under Review')
            print(f"Processing application: {app.name}")
            return app
        else:
            print("No applications to process")

    # Task 3 - Shortlist or Reject
    def shortlist_application(self, app):
        app.status = 'Shortlisted'
        self.recent_activity_stack.append(app)
        self.application_tracking[app.name].append('Shortlisted')
        print(f"{app.name} shortlisted")

    def reject_application(self, app):
        app.status = 'Rejected'
        self.recent_activity_stack.append(app)
        self.application_tracking[app.name].append('Rejected')
        print(f"{app.name} rejected")

    # Task 4 - Partial Search by name or job ID
    def search_application(self):
        query = input("Enter search term (partial match allowed): ").lower()
        results = [app for app in self.applications if query in app.name.lower() or query in app.job_id.lower()]
        for app in results:
            print(app)
        if not results:
            print("No applications found")

    # CRUD Operations
    def update_application(self):
        name = input("Enter applicant name to update: ")
        for app in self.applications:
            if app.name == name:
                new_status = input("Enter new status (Shortlisted/Rejected): ")
                app.status = new_status
                self.application_tracking[app.name].append(new_status)
                print(f"Application status updated for {app.name}")
                return
        print("Application not found")

    def delete_application(self):
        name = input("Enter applicant name to delete: ")
        self.applications = [app for app in self.applications if app.name != name]
        self.application_queue = [app for app in self.application_queue if app.name != name]
        self.application_tracking.pop(name, None)
        print(f"Application deleted for {name}")

    # Task 6 - Report Generation
    def generate_report(self):
        total_apps = len(self.applications)
        status_count = {"Shortlisted": 0, "Rejected": 0, "Submitted": 0, "Under Review": 0}
        jobs_count = {}

        for app in self.applications:
            status_count[app.status] += 1
            if app.job_id in jobs_count:
                jobs_count[app.job_id] += 1
            else:
                jobs_count[app.job_id] = 1

        print("Total Applications:", total_apps)
        print("Applications by Status:", status_count)
        print("Applications by Job Position:", jobs_count)

    def menu(self):
        while True:
            print("\n--- Application Management System Menu ---")
            print("1. Submit Application")
            print("2. Process Application")
            print("3. Search Application")
            print("4. Update Application")
            print("5. Delete Application")
            print("6. Generate Report")
            print("7. Exit")

            choice = input("Enter your choice: ")
            if choice == '1':
                self.submit_application()
            elif choice == '2':
                app = self.process_application()
                if app:
                    decision = input("Shortlist or Reject? (s/r): ").lower()
                    if decision == 's':
                        self.shortlist_application(app)
                    elif decision == 'r':
                        self.reject_application(app)
            elif choice == '3':
                self.search_application()
            elif choice == '4':
                self.update_application()
            elif choice == '5':
                self.delete_application()
            elif choice == '6':
                self.generate_report()
            elif choice == '7':
                break
            else:
                print("Invalid choice, please try again")

# Example Usage
if __name__ == "__main__":
    system = ApplicationManagementSystem()
    system.menu()
