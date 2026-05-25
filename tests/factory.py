from django.contrib.auth import get_user_model
from factory import Faker, LazyAttribute, fuzzy, post_generation
from factory.django import DjangoModelFactory

User = get_user_model()

class UserFactory(DjangoModelFactory):
    username = LazyAttribute(
        lambda obj: "{}_{}_{}".format(
            obj.first_name.lower().replace(" ", ""),
            obj.last_name.lower().replace(" ", ""),
            fuzzy.FuzzyInteger(0, 99999).fuzz(),
        )
    )
    email = LazyAttribute(lambda obj: "%s@gmail.com" % obj.username)
    first_name = Faker("name")
    last_name = Faker("name")

    @post_generation
    def password(self, create, extracted, **kwargs):
        password = (
            extracted
            if extracted
            else Faker(
                "password",
                length=42,
                special_chars=True,
                digits=True,
                upper_case=True,
                lower_case=True,
            ).evaluate(None, None, extra={"locale": None})
        )
        self.set_password(password)

    @post_generation
    def groups(self, create, extracted, **kwargs):
        if not create:
            return

        if extracted:
            for group in extracted:
                self.groups.add(group)

    class Meta:
        model = User
        django_get_or_create = ["username"]
