# /// script
# requires-python = ">=3.11"
# dependencies = [
#     "feedparser",
#     "python-dateutil",
# ]
# ///
import feedparser
import datetime
from typing import List, Dict
import re

def parse_date(date_string: str) -> str:
    """Parse date string and return formatted date."""
    try:
        # Try parsing different date formats
        for fmt in ['%a, %d %b %Y %H:%M:%S %z', '%Y-%m-%dT%H:%M:%S%z', '%Y-%m-%d']:
            try:
                dt = datetime.datetime.strptime(date_string.split('.')[0], fmt)
                return dt.strftime('%B %d, %Y')
            except:
                continue
    except:
        pass
    return ''

def fetch_feed_posts(feed_url: str, source_name: str, max_posts: int = 3) -> List[Dict]:
    """Fetch recent posts from an RSS feed."""
    posts = []
    try:
        feed = feedparser.parse(feed_url)
        for entry in feed.entries[:max_posts]:
            date_str = entry.get('published', entry.get('updated', ''))
            posts.append({
                'title': entry.title,
                'link': entry.link,
                'date': parse_date(date_str),
                'source': source_name
            })
    except Exception as e:
        print(f"Error fetching {source_name}: {e}")
    return posts

def update_readme():
    """Update README.md with latest blog posts."""
    
    # Fetch posts from both feeds
    personal_posts = fetch_feed_posts(
        'https://fz42.net/posts/feed.xml',
        'FatZombi',
        max_posts=3
    )
    
    corporate_posts = fetch_feed_posts(
        'https://blog.stratumsecurity.com/author/phil/rss',
        'Stratum Security',
        max_posts=3
    )
    
    # Read current README
    with open('README.md', 'r') as f:
        readme = f.read()
    
    # Find the section to update (between markers)
    start_marker = '<!-- BLOG-POST-LIST:START -->'
    end_marker = '<!-- BLOG-POST-LIST:END -->'
    
    start_index = readme.find(start_marker)
    end_index = readme.find(end_marker)
    
    if start_index == -1 or end_index == -1:
        print("Markers not found in README. Please add them.")
        return
    
    # Generate new content
    new_content = start_marker + '\n\n'
    
    # Personal posts section
    if personal_posts:
        new_content += "I write about technology, security, and software engineering on my [**personal blog**](https://fz42.net):\n\n"
        for post in personal_posts:
            date_sub = f" <sub><em>{post['date']}</em></sub>" if post['date'] else ""
            new_content += f"* 🔧 [{post['title']}]({post['link']}){date_sub}\n"
    
    new_content += "\n---\n\n"
    
    # Corporate posts section
    if corporate_posts:
        new_content += "I also contribute to [**Stratum Security's blog**](https://blog.stratumsecurity.com) where I write about security research and consulting:\n\n"
        for post in corporate_posts:
            date_sub = f" <sub><em>{post['date']}</em></sub>" if post['date'] else ""
            new_content += f"* 🛡️ [{post['title']}]({post['link']}){date_sub}\n"
    
    new_content += '\n' + end_marker
    
    # Update README
    new_readme = readme[:start_index] + new_content + readme[end_index + len(end_marker):]
    
    # Update last updated timestamp
    timestamp_marker = '<!-- LAST-UPDATED -->'
    if timestamp_marker in new_readme:
        current_date = datetime.datetime.now().strftime('%B %d, %Y')
        new_readme = re.sub(
            r'<!-- LAST-UPDATED -->.*?(?=<|$)', 
            f'<!-- LAST-UPDATED -->{current_date}', 
            new_readme
        )
    
    with open('README.md', 'w') as f:
        f.write(new_readme)
    
    print("README updated successfully!")

if __name__ == "__main__":
    update_readme()