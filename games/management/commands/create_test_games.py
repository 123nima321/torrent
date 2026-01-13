import random
from io import BytesIO
from django.core.management.base import BaseCommand
from django.core.files.base import ContentFile
from PIL import Image, ImageDraw
from games.models import Game

class Command(BaseCommand):
    help = 'Creates test games with random data and placeholder images'

    def add_arguments(self, parser):
        parser.add_argument(
            '--delete',
            action='store_true',
            help='Delete all existing games before creating new ones',
        )
        parser.add_argument(
            '--count',
            type=int,
            default=10,
            help='Number of games to create',
        )

    def handle(self, *args, **options):
        if options['delete']:
            self.stdout.write('Deleting existing games...')
            Game.objects.all().delete()

        count = options['count']
        self.stdout.write(f'Creating {count} test games...')

        games_data = [
            {
                'name': 'Кибер Прорыв 2077',
                'description': 'Захватывающий экшен в открытом мире будущего. Исследуйте неоновый город, сражайтесь с корпорациями и улучшайте своего персонажа.',
                'category': 'Action',
                'platform': 'PC',
                'memory': 70.0,
            },
            {
                'name': 'Ведьмак: Легенды',
                'description': 'Эпическая ролевая игра в фэнтезийном мире. Охотьтесь на чудовищ, принимайте сложные решения и влияйте на судьбу королевств.',
                'category': 'RPG',
                'platform': 'Xbox',
                'memory': 50.5,
            },
            {
                'name': 'Звездная Стратегия',
                'description': 'Постройте свою галактическую империю. Управляйте флотами, развивайте технологии и дипломатию в этой глубокой стратегии.',
                'category': 'Strategy',
                'platform': 'PC',
                'memory': 15.0,
            },
            {
                'name': 'Скорость и Ярость',
                'description': 'Адреналиновые гонки по улицам ночного города. Тюнинг автомобилей, реалистичная физика и напряженные соревнования.',
                'category': 'Racing',
                'platform': 'PS',
                'memory': 25.0,
            },
            {
                'name': 'Футбольный Менеджер 2025',
                'description': 'Управляйте любимым футбольным клубом. Трансферы, тактика, тренировки - все в ваших руках.',
                'category': 'Sports',
                'platform': 'Mobile',
                'memory': 2.5,
            },
            {
                'name': 'Ужас в Глубинах',
                'description': 'Атмосферный хоррор о выживании на заброшенной подводной станции. Раскройте тайны и постарайтесь не сойти с ума.',
                'category': 'Horror',
                'platform': 'PC',
                'memory': 12.0,
            },
            {
                'name': 'Лесные Приключения',
                'description': 'Милая адвенчура о путешествии маленького духа через волшебный лес. Решайте головоломки и помогайте лесным жителям.',
                'category': 'Adventure',
                'platform': 'Switch',
                'memory': 3.5,
            },
            {
                'name': 'Битва Героев',
                'description': 'Многопользовательская арена, где сражаются легендарные герои. Командная тактика и индивидуальное мастерство.',
                'category': 'MMO',
                'platform': 'PC',
                'memory': 40.0,
            },
            {
                'name': 'Симулятор Фермера',
                'description': 'Расслабляющий симулятор жизни на ферме. Выращивайте урожай, ухаживайте за животными и развивайте свое хозяйство.',
                'category': 'Simulation',
                'platform': 'PC',
                'memory': 8.0,
            },
            {
                'name': 'Тетрис 3D',
                'description': 'Новый взгляд на классическую головоломку. Трехмерные фигуры, новые режимы и красочные эффекты.',
                'category': 'Puzzle',
                'platform': 'Mobile',
                'memory': 0.5,
            }
        ]

        def create_placeholder_image(color):
            img = Image.new('RGB', (600, 400), color=color)
            draw = ImageDraw.Draw(img)
            # Add some noise/pattern
            for _ in range(50):
                x = random.randint(0, 600)
                y = random.randint(0, 400)
                r = random.randint(5, 50)
                draw.ellipse((x-r, y-r, x+r, y+r), fill=(255, 255, 255, 30))
            
            output = BytesIO()
            img.save(output, format='JPEG', quality=85)
            return output

        created_count = 0
        for i in range(count):
            base_data = random.choice(games_data)
            # Add some randomization to avoid duplicates if creating many
            suffix = "" if i < len(games_data) else f" {i}"
            
            game = Game(
                name=f"{base_data['name']}{suffix}",
                description=base_data['description'],
                category=base_data['category'],
                platform=base_data['platform'],
                memory=base_data['memory'] + random.uniform(-0.5, 0.5)
            )

            # Generate random color for image
            color = (random.randint(50, 200), random.randint(50, 200), random.randint(50, 200))
            image_content = create_placeholder_image(color)
            
            filename = f"game_{i}_{random.randint(1000, 9999)}.jpg"
            game.image.save(filename, ContentFile(image_content.getvalue()), save=False)
            
            game.save()
            created_count += 1
            self.stdout.write(f'Created game: {game.name}')

        self.stdout.write(self.style.SUCCESS(f'Successfully created {created_count} games'))
