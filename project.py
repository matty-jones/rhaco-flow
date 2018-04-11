import flow


class LynxProject(flow.FlowProject):
    def __init__(self, *args, **kwargs):
        super(LynxProject, self).__init__(*args, **kwargs)
        self.add_operation(
            name='pipeline',
            cmd=lambda job: "python operations.py pipeline {}".format(job),
            post=[LynxProject.generated]
        )
        self.add_operation(
            name='generate',
            cmd=lambda job: "python operations.py generate {}".format(job),
            post=[LynxProject.generated]
        )
        self.add_operation(
            name='simulate',
            cmd=lambda job: "python -u operations.py simulate {}".format(job),
            pre=[LynxProject.generated],
            post=[LynxProject.simulated]
        )

    @flow.staticlabel()
    def generated(job):
        return job.isfile('output.hoomdxml')

    @flow.staticlabel()
    def simulated(job):
        return job.isfile('output_traj.gsd')


if __name__ == '__main__':
    LynxProject().main()
