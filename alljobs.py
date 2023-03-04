@app.route('/alljobs')
def all_jobs():
    dbs = db_session.create_session()
    if current_user.is_authenticated:
        res = dbs.query(Jobs).filter((Jobs.team_leader.like(current_user.id) | Jobs.collaborators.like(f'%{current_user.id}%')))
        jobs = []
        for el in res:
            title = el.job
            time = el.end_date - el.start_date
            print(el, "-", time)
            team_leader = f"{el.user.name} {el.user.surname}"
            collaborators = el.collaborators
            isf = el.is_finished
            lvl = el.hazard_level[-1].level
            jobs.append([title, team_leader, time, collaborators, isf, el.user.id, el.id, lvl])
        return render_template('alljobs.html', jobs=jobs)
    else:
        pass
