from src.resources import resource


class SkillPoint(resource.Resource):

    @classmethod
    def create(cls, count=0):
        print cls
        return cls(resource_type="skill_point", count=count)


class PoolSkillPoint(SkillPoint):
    pass
