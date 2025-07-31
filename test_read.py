from website import WebsiteTools

wt = WebsiteTools()
content = wt.read_url("https://www.espn.com/nfl/team/injuries/_/name/mia/miami-dolphins")
print(content)
