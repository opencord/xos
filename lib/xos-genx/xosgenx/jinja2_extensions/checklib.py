import ast

def xproto_check_synchronizer(m):
    try:
        sync_step_path = 'synchronizer/steps/sync_%s.py'%m['name'].lower()
        sync_step = open(sync_step_path).read()
    except IOError:
        return '510 Model needs a sync step %s'%sync_step_path

    try:
        sync_step_ast = ast.parse(sync_step)
    except SyntaxError:
        return '511 Could not parse sync step %s'%sync_step_path

    classes = filter(lambda x:isinstance(x, ast.ClassDef), sync_step_ast.body)
    found_sync_step_class = False

    for c in classes:
        base_names = [v.id for v in c.bases]
        if 'SyncStep' in base_names or 'SyncInstanceUsingAnsible' in base_names:
            attributes = filter(lambda x:isinstance(x, ast.Assign), c.body)
            for a in attributes:
                target_names = [t.id for t in a.targets]
                values = a.value.elts if isinstance(a.value, ast.List) else [a.value]
                value_names = [v.id for v in values]

                if 'observes' in target_names and m['name'] in value_names:
                    found_sync_step_class = True
                    break

    if not found_sync_step_class:
        return '512 Synchronizer needs a sync step class with an observes field containing %s'%m['name']
    else:
        return '200 OK'


def xproto_check_policy(m):
    try:
        model_policy_path = 'synchronizer/model_policies/model_policy_%s.py'%m['name'].lower()
        model_policy = open(model_policy_path).read()
    except IOError:
        return '510 Model needs a model policy %s'%model_policy_path

    try:
        model_policy_ast = ast.parse(model_policy)
    except SyntaxError:
        return '511 Could not parse sync step %s'%model_policy_path

    classes = filter(lambda x:isinstance(x, ast.ClassDef), model_policy_ast.body)
    found_model_policy_class = False
    for c in classes:
        base_names = [v.id for v in c.bases]
        if 'Policy' in base_names or 'TenantWithContainerPolicy' in base_names:
            found_model_policy_class = True
            break

    if not found_model_policy_class:
        return '513 Synchronizer needs a model policy class'
    else:
        return '200 OK'

