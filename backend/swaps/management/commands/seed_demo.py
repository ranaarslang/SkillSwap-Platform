from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from swaps.models import Profile

DEMO = [
    ("maya", "Maya Chen", "Product designer teaching Figma and design systems.", ["Product design", "Figma", "Design systems"], ["React", "Storytelling"], "#f2b84b"),
    ("jonah", "Jonah Williams", "Frontend engineer who loves making complex things feel simple.", ["React", "TypeScript", "Accessibility"], ["Photography", "Figma"], "#98c7b8"),
    ("sana", "Sana Patel", "Data storyteller turning messy questions into clear decisions.", ["Python", "Data visualization", "SQL"], ["Public speaking", "Brand strategy"], "#d7a7bc"),
    ("leo", "Leo Martins", "Independent filmmaker, editor, and curious lifelong learner.", ["Video editing", "Storytelling", "Motion design"], ["Product design", "Python"], "#b4a6d5"),
]

class Command(BaseCommand):
    help = "Create demo SkillSwap users and profiles"
    def handle(self, *args, **kwargs):
        for username, name, bio, offered, wanted, color in DEMO:
            first, last = name.split(" ", 1)
            user, created = User.objects.get_or_create(username=username, defaults={"first_name": first, "last_name": last})
            if created: user.set_password("demo1234"); user.save()
            Profile.objects.update_or_create(user=user, defaults={"bio": bio, "skills_offered": offered, "skills_wanted": wanted, "is_verified": True, "avatar_color": color, "portfolio_links": ["https://example.com"]})
        self.stdout.write(self.style.SUCCESS("Demo data ready. Login with maya / demo1234."))
