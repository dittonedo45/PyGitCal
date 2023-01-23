#include <git2.h>
#include <python3.8/Python.h>

static int
calculate_commits (char* path, int (*cb)(void *dptr,
			time_t), void *dptr)
{
	git_repository* rp;
	if (git_repository_open (&rp, path))
		return 1;
	do {
				git_revwalk *revwalk = 0;

				git_revwalk_new (&revwalk, rp);
				git_revwalk_push_head (revwalk);

				while (1)
				{
					git_oid oid;
					git_commit* cmt;

					int
					ret = git_revwalk_next (&oid, revwalk);
					if (ret==GIT_ITEROVER) break;
					if (!git_commit_lookup (&cmt, rp, &oid))
					{
						if (cb && dptr)
							cb(dptr, git_commit_time (cmt));
						git_commit_free (cmt);
					}
				}
				git_revwalk_free (revwalk);
	} while (0);
	git_repository_free (rp);
}

int
fill_table_cb_ins (void *dptr, time_t t)
{
	PyList_Append ( (PyObject*)dptr,
			PyLong_FromUnsignedLong(t));
	return 0;
}

int
main(int argsc, char **args)
{
	Py_InitializeEx (0);
	git_libgit2_init ();
	PyConfig conf;
	PyConfig_InitPythonConfig (&conf);
	PyConfig_SetBytesArgv (&conf, argsc, args);

	PyObject* obj=PyList_New(0);
	calculate_commits (args[2], fill_table_cb_ins, obj);
	Py_XINCREF (obj);
	PySys_SetObject ("history", obj);
	FILE *fp=fopen (args[1], "r");
	if (fp)
	{
		PyRun_AnyFile (fp, args[1]);
		fclose (fp);
	}
	git_libgit2_shutdown ();
	Py_Finalize ();
	return 0;
}
