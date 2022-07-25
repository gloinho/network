from django.test import TestCase
from network.models import User, Post, Connections, Comment

# Create your tests here.
class ConnectionTestCase(TestCase):
    def setUp(self):
        
        # Creating users
        u1 = User.objects.create(username='u1')
        u2 = User.objects.create(username='u2')
        u3 = User.objects.create(username='u3')
        
        # Creating posts
        p1 = Post.objects.create(posted_by=u1, content='testing u1 post')
        p2 = Post.objects.create(posted_by=u3, content='testing u3 post')
        
    def test_creating_new_connection(self):
        
        u1 = User.objects.get(username='u1')
        c1 = Connections.objects.create(user=u1)
        
        self.assertEqual(u1, c1.user)
    
    def test_post_content_cannot_be_blank(self):
        u2 = User.objects.get(username='u2')
        p2 = Post.objects.create(posted_by=u2)
        
        self.assertTrue(p2.is_content_empty)
        
    def test_connection_exists(self):
        u1 = User.objects.get(username='u1')
        c1 = Connections.objects.create(user=u1)
        self.assertTrue(Connections.objects.get(user=u1))
        
        
    
        