CMSC388J Final Project Proposal


List all project members' names: Henry Wang, Viraj Patel, Gordon Wu


General description of project: This project will essentially be a review website for football players in regards to fantasy football. Players will have their own individual pages that users can search for that display fantasy football stats for that player and include some general top production stats and potentially even videos for their best performances. Users will be able to comment when these players should be drafted in future fantasy football drafts and provide reviews on these players as fantasy football players. There will also be a like/dislike system on these reviews, and those users with the highest amount of likes will be considered verified reviewers so that when reviews are viewed, users can see that these reviews hold more weight.


How each requirement will be satisfied:


* Registration & Login
   * This is essentially like a fantasy football review kind of website, where fantasy football users could review football players in regards to their fantasy worth. We can create a likes system where users who obtain the most likes can almost become slightly more important in regards to their reviews.
   * Mandatory two-factor authentication for all users to login to accounts
* Forms
   * Forms can be used to create reviews for specific players. Also registration and logging in.
* Database
   * MongoDB will be used to store all reviews and notable information that are collected by Forms.
* Security
   * Utilize security measures learned in the course, such as CSRF-protection for all forms we use, as well as other guidelines described in the project requirements for the appropriate components of our web application
* Blueprints
   * Our first set of blueprints will be splitting up the routes.py file into different blueprints based off of user management player profile pages and comments. We can also have another separate blueprint for static content for information that could be shown on the homepage
* Presentation
   * Utilize Bootstrap to develop well-designed and formatted web pages in HTML and CSS
* Use of new Python package
   * We will be using Requests at the very minimum to obtain our data from a fantasy football API (ESPN, etc.). We may also use Pandas for statistical analysis.
* Evidence of usage
   * The website will contain sample users and accounts that have engaged in most of the core interactions and functions of the website, including user-written reviews and user discussions