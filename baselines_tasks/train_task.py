import luigi

from unl_luigi.tasks.shell_task import ShellTask


class TrainTask(ShellTask):
    env_type = luigi.Parameter()
    env = luigi.Parameter()
    constraint = luigi.Parameter()
    reward_shaping = luigi.IntParameter()
    augmentation = luigi.Parameter()
    seed = luigi.IntParameter()

    def run(self):
        cmd_str = 'OPENAI_LOGDIR="./openai_log/${SLURM_JOBID}" python -m baselines.run'
        cmd_str += ' --env ' + str(self.env)
        if self.env_type == 'atari':
            cmd_str += ' --alg deepq'
            cmd_str += ' --num_timesteps 1e7'
        elif self.env_type == 'mujoco':
            cmd_str += ' --alg ppo2'
            cmd_str += ' --num_timesteps 1e6'
        if constraint:
            cmd_str += ' --constraints ' + str(self.constraint)
            cmd_str += ' augmentation ' + str(self.reward_shaping)
        if self.augmentation:
            cmd_str += ' --augmentation ' + str(self.augmentation)

        print(cmd_str)
        #self.run_command()
