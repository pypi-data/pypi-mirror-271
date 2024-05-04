def test_number_1(about_project):
    name, version = about_project
    assert name == 'xnippy'
    assert version == '0.1.0'
    
def test_config(about_project):
    pass