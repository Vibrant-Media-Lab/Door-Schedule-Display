import HTMLScraper
import DisplayRefresher


def main():
    # Fetch the Lab Hours from the Google Doc
    HTMLScraper.fetch_hours_from_google_doc()

    # Update the display with the fetched hours
    DisplayRefresher.update_display()
