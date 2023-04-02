from projects.models import Project
from voting.models import Candidate

Project.objects.bulk_create([
    Project(title='My First Project', description='A web development project.', technology='Django',
            image='img/.png'),
    
])

Candidate.objects.bulk_create([
    Candidate(
        name='Klaus Werner Iohannis',
        description='Leader of PNL, '
                    'Mayor of Siubiu.',
        image='img/iohannis.png'
    ),
    Candidate(
        name='Vasilica Viorica Dăncilă',
        description='President of the PSD',
        image='img/dancila.png'
    )
])
