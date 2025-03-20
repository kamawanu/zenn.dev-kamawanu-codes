from django.db.migrations import Migration


class MultiMigrationMeta(type(Migration)):
    def __new__(mcs, name, bases, attrs):
        merged_dependencies = []
        merged_operations = []
        # 継承元クラスからマージ
        for base in bases:
            if hasattr(base, 'dependencies'):
                merged_dependencies += base.dependencies
            if hasattr(base, 'operations'):
                merged_operations += base.operations
        # 自クラス定義の内容もマージ
        merged_dependencies += attrs.get('dependencies', [])
        merged_operations += attrs.get('operations', [])
        attrs['dependencies'] = merged_dependencies
        attrs['operations'] = merged_operations
        return super().__new__(mcs, name, bases, attrs)


class CombinedMigration(Migration, metaclass=MultiMigrationMeta):
    """
    このクラスをベースにすると、以下のように
    複数の Migration クラスを多重継承して、
    dependencies や operations がマージされます。

    例:
      class BaseMigrationA(Migration):
          dependencies = [('app', '0001_initial')]
          operations = [
              # 何らかの操作 A
          ]

      class BaseMigrationB(Migration):
          dependencies = [('app', '0002_auto')]
          operations = [
              # 何らかの操作 B
          ]

      class MyMigration(CombinedMigration, BaseMigrationA, BaseMigrationB):
          dependencies = [('app', '0003_some_migration')]
          operations = [
              # 追加の操作
          ]

    この場合、MyMigration の dependencies と operations には、
    BaseMigrationA, BaseMigrationB、および MyMigration 自身の内容が全て含まれます。
    """
    pass
