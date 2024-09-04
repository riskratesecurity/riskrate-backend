from riskrate_backend.model.models import License


def test_create_license(db_session):
    license = License(
        code="LIC123",
        name="Pro License",
        description="A professional license with extended features",
        duration=365,
        features={"feature_1": "value_1", "feature_2": "value_2"},
    )

    db_session.add(license)
    db_session.commit()
    db_session.refresh(license)

    assert license.id is not None
    assert license.code == "LIC123"
    assert license.name == "Pro License"
    assert license.duration == 365
    assert license.features == {"feature_1": "value_1", "feature_2": "value_2"}
