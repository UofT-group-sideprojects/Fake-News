# Fake News
This Chrome Extension uses the metadata of an article and calculates how likely it is to have quality content

Ambition Level of this project: 6/10

<h2>The idea:</h2> 
<p>
The idea is, given a webpage that has an article on it. This app will read Meta Data such as <br>
-The Author <br>
-The sources <br>
-The site it is hosted on <br>
... To be added to <br>
and then represent on a scale how likely this article is to be reliable.

For instance, if an article is written by an author that works for <strong>The Economist</strong>, their sources are also by well established reporters and the site it is published on is trusted. The article will be marked as likely to contain reliable information.

However, if an article is written by an Author who writes for <strong>The Onion</strong>, they have no sources and the article is posted on the onion. It will be marked as unreliable.
</p>

<h2>What needs to be done:</h2>
<p>
-WebScraper: <br>
    &emsp; -search through the text on a page for words that match a regex <br>
-API search:<br>
    &emsp; -Find an API that returns an authors reputation (Alternatively if they are peer reviewed or other criterea) <br>
    &emsp; -Find an API that returns the reputation of a site (Minimum Viable product, hard code some site reliabilities) <br>
-API implementation: <br>
    &emsp; -Connect to API <br>
-Chrome Extension: <br>
    &emsp; -Build a Chrome Extension <br>
    &emsp; -Connect the Webscraper to the current page with a button to 'Scrape' <br>
    &emsp; -Once scraped, connect the scraped results to the API Implementation <br>
 </p>
<br>
<h2>Knowledge required (We can learn as we go):</h2>
<p>
-WebScraper: <br>
    &emsp; -Python <br>
    &emsp; -Beautiful Soup <br>
    &emsp; -Regular Expressions <br>
    &emsp; -Unknowns <br>
    &emsp; -A useful walk through:  https://first-web-scraper.readthedocs.io/en/latest/ <br>
-API search:<br>
    &emsp; -Understand how API's work and API endpoints <br>
-API implementation: <br>
    &emsp; -Connect to API (probably with Javascript) <br>
-Chrome Extension: <br>
    &emsp; -JavaScript <br>
    &emsp; -JSON (Simple) <br>
    &emsp; -useful link https://developer.chrome.com/extensions/getstarted <br>
</p>

<h2>Project Board</h2>
<p>
https://github.com/orgs/UofT-group-sideprojects/projects/2  <br>
</p>
<h2>Contact</h2>
<p>
  Project Owner: <strong>Daniel Visca</strong> <br>
  email: <strong>daniel.visca@mail.utoronto.ca</strong> <br> 
  phone number: <strong> +1 (514) 889-6686 </strong> <br>
  <br>
  If you would like any clarification, or would like to get together in person to work on this please reach out!
</p>
