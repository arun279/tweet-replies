import unittest
from tweet_replies import TweetReplies

class TestTweetReplies(unittest.TestCase):

    def setUp(self):
        self.tweet_replies = TweetReplies()

    def test_extract_handle(self):
        # Test with a sample tweet HTML that contains the handle
        tweet_html = '<div class="css-901oao r-1bwzh9t r-37j5jr r-a023e6 r-16dba41 r-rjixqe r-bcqeeo r-qvutc0">' \
                     '<a href="/handle"><span>handle</span></a>' \
                     '</div>'
        handle = self.tweet_replies.extract_handle(tweet_html)
        self.assertEqual(handle, 'handle')
        
        # Test with a sample tweet HTML that doesn't contain the handle
        tweet_html = '<div class="css-901oao r-1bwzh9t r-37j5jr r-a023e6 r-16dba41 r-rjixqe r-bcqeeo r-qvutc0"></div>'
        handle = self.tweet_replies.extract_handle(tweet_html)
        self.assertIsNone(handle)

    def test_extract_content(self):
        pass

    def test_extract_url(self):
        pass

    def test_scroll_load(self):
        pass

if __name__ == '__main__':
    unittest.main()
