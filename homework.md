# Philosophy game

---

## What is it ?

[See wikipedia article](https://en.wikipedia.org/wiki/Wikipedia:Getting_to_Philosophy)

Clicking on the first link in the main text of a Wikipedia article, and then repeating the process for subsequent articles, would usually lead to the Philosophy article. As of February 2016, 97% of all articles in Wikipedia eventually led to the article Philosophy.

The remaining articles lead to an article without any outgoing wikilinks, to pages that do not exist, or get stuck in loops. This has gone up from 94.52% in 2011. At some point in the past the median link chain length to reach philosophy was 23.

## Method:

Following the chain consists of:

- Clicking on the first non-parenthesized, non-italicized link
- Ignoring external links, links to the current page, or red links (links to non-existent pages)
- Stopping when reaching "Philosophy", a page with no links or a page that does not exist, or when a loop occurs

---
## To Do

- Do a `frontend` where user can provide a wiki link.
- Backend will follow the rules and find (or not) the philosophy page. Then respond with the followed path.
- `frontend` should show the path nicely. And make it easily explorable.

- Add a `README` where you explain your approach.
- Provide everything in a git repo with an easy start.sh command for launching the app.

## Extra Optional features

- Provide a way to find the shorter path to the philosophy page, this means you have to break the rules and not only follow the first valid link. And compare it with the previous response which follows the rules.
- Provide a way to submit bulk wiki links and visualise the bulk links graph up to the philosophy page.
- Provide a way to change the target page (not only philosophy, maybe pokemon page may work too).

## Technology Requirements

- `Python` backend for api and scraping
- `React` frontend and you can serve it with node or nginx.
- Wrap everything in `Docker` containers and orchestrate them with `docker-compose`.
- Only a dev env is required.

## Questions

We want to deploy this app on a server in the cloud:

- Provide next steps and recommendations for a prod deployment in a bullet point list.

We want to think about version 2.0 of this app:

- What features would you add ?
