import luigi
import os
from unl_luigi.config.blackhole import BlackholeConfig
from unl_luigi.tasks.shell_task import ShellTask


class CheckpointDatabase(ShellTask):
    database_path = luigi.Parameter()

    def __init__(self, *args, **kwargs):
        super(CheckpointDatabase, self).__init__(*args, **kwargs)
        self.instance_name = "CheckpointDatabase_%s" % self.database_path

    def output(self):
        return luigi.LocalTarget(self.database_path +
                                 "_tasks/checkpoint.success")

    def run(self):
        blackhole_app_path = BlackholeConfig().blackhole_app
        command = "%s -c crane_checkpoint { -d %s }" % (blackhole_app_path,
                                                        self.database_path)
        (returncode, stdout, stderr) = self.run_command(command)

        base_path = "%s_tasks" % self.database_path
        if not os.path.exists(base_path):
            os.makedirs(base_path)

        with open("%s/checkpoint.retcode" % base_path, 'w') as out_file:
            out_file.write(str(returncode))
        with open("%s/checkpoint.out" % base_path, 'w') as out_file:
            out_file.write(stdout.decode("utf-8"))
        with open("%s/checkpoint.err" % base_path, 'w') as out_file:
            out_file.write(stderr.decode("utf-8"))

        if returncode > 0:
            raise Exception(
                "Received error code %s in CheckpointDatabase: %s" %
                (returncode, self.database_path))

        with self.output().open('w') as out_file:
            out_file.write("1")
