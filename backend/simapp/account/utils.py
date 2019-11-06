from django.utils.translation import ugettext_lazy as _

GENDER_CHOICES = (
    ('NotSet', 'NotSet'),
    ('Male', 'Male'),
    ('Female', 'Female')
)

DEFAULT_USER_GENDER = 'NotSet'

NOTIFICATION_TYPES = (
    ('enabled', 'Enabled notifications'),
    ('email', 'Email only'),
    ('push', 'Push only'),
    ('disabled','Disabled notifications')

)


AREA_CHOICES = (
    ('JERUSALEM',"Jerusalem district"),
    ("NORTH","North district"),
    ("HAIFA","Haifa district"),
    ('CENTRAL',"Central district"),
    ('TEL-AVIV','Tel-Aviv district'),
    ('SOUTHERN','Southern district'),
    ("JUDEA-SAMARIA",'Judea and Samaria district')
                )


SPECIALIZATION_CHOICES = (

    ("INTERNAL-MEDICINE-PHYSICIAN","Internal Medicine Physician"),
    ("PEDIATRICIAN","Pediatrician"),
    ("OBSTETRICIAN-GYNECOLOGIST","Obstetrician/Gynecologist"),
    ("SURGEON","Surgeon"),
    ("PSYCHIATRIST","Psychiatrist"),
    ("CARDIOLOGIST","Cardiologist"),
    ("DERMATOLOGIST","Dermatologist"),
    ("ENDOCRINOLOGIST","Endocrinologist"),
    ("GASTROENTEROLOGIST","Gastroenterologist"),
    ("INFECTIOUS-DISEASE-PHYSICIAN ","Infectious Disease Physician"),
    ("NEPHROLOGIST","Nephrologist"),
    ("OPHTHALMOLOGIST","Ophthalmologist"),
    ("OTOLARYNGOLOGIST","Otolaryngologist"),
    ("PULMONOLOGIST","Pulmonologist"),
    ("NEUROLOGIST","Neurologist"),
    ("PHYSICIAN-EXECUTIVE ","Physician Executive"),
    ("RADIOLOGIST","Radiologist"),
    ("ANESTHESIOLOGIST","Anesthesiologist"),
    ("ONCOLOGIST","Oncologist")
                        )