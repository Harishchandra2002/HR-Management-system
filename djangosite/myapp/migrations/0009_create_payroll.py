from django.db import migrations, models
import django.utils.timezone

class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0008_alter_leaverequest_end_date_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Payroll',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('attendance', models.IntegerField()),
                ('leaves', models.IntegerField()),
                ('basic_salary', models.DecimalField(decimal_places=2, max_digits=10)),
                ('deductions', models.DecimalField(decimal_places=2, max_digits=10)),
                ('pay_date', models.DateField(default=django.utils.timezone.now)),
                ('employee', models.ForeignKey(on_delete=models.CASCADE, to='myapp.Employee_Data')),
            ],
            options={
                'db_table': 'payroll',
            },
        ),
        migrations.CreateModel(
            name='Goal',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.TextField()),
                ('deadline', models.DateField()),
                ('achieved', models.BooleanField(default=False)),
            ],
            options={
                'db_table': 'goal',
            },
        ),
        migrations.CreateModel(
            name='PerformanceReview',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rating', models.IntegerField()),
                ('feedback', models.TextField()),
                ('goal', models.ForeignKey(on_delete=models.CASCADE, to='myapp.Goal')),
            ],
            options={
                'db_table': 'performance_review',
            },
        ),
        migrations.CreateModel(
            name='DevelopmentPlan',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('program_name', models.CharField(max_length=100)),
                ('description', models.TextField()),
            ],
            options={
                'db_table': 'development_plan',
            },
        ),
    ]
