from urllib.parse import quote

class SocialMediaService:
    def get_sharing_url(self, platform, post):
        base_url = "http://127.0.0.1:5000/"  # Replace with your actual domain
        post_url = f"{base_url}/post/{post.id}"
        
        # Create message based on post type
        if post.type == "lost":
            title = "I lost an item and the information of the item is as follows:"
            call_to_action = "\n\nPlease let me know if you have found this item!"
        else:
            title = "I found an item and the information of the item is as follows:"
            call_to_action = "\n\nIf this is your item, please verify and claim ownership through the link below."
            
        details = (f"\nItem Name: {post.item_name}"
                  f"\nLocation: {post.location}"
                  f"\nCategory: {post.category_name}"
                  f"\nDescription: {post.description}")
        
        if platform == "facebook":
            full_message = title + details + call_to_action
            return f"https://www.facebook.com/sharer/sharer.php?u={quote(post_url)}&quote={quote(full_message)}"
            
        elif platform == "twitter":
            tweet_text = f"{title}{details[:100]}...{call_to_action}"
            return f"https://twitter.com/intent/tweet?text={quote(tweet_text)}&url={quote(post_url)}"
            
        elif platform == "whatsapp":
            message = f"{title}{details}{call_to_action}\n\nView details: {post_url}"
            return f"https://wa.me/?text={quote(message)}"
            
        elif platform == "telegram":
            message = f"{title}{details}{call_to_action}\n\nView details: {post_url}"
            return f"https://t.me/share/url?url={quote(post_url)}&text={quote(message)}"
            
        return None
