"""Finite learned communication experiment. See PREREG.md for claim limits."""
import itertools
import numpy as np

SEEDS = (41, 97, 127, 203, 509)


def dataset():
    w, a, b, u, v = np.array(list(itertools.product((-1., 1.), repeat=5))).T
    return {'s': np.c_[a, b, w*a*b], 'q': np.c_[u, v],
            'y': (w*u*v+1)/2, 'w': w,
            'train': ~((u == a) & (v == a*b))}


def sigmoid(z):
    return np.exp(-np.logaddexp(0, -z))


class MLP:
    def __init__(self, inputs, hidden, rng):
        self.hidden = hidden
        if hidden:
            self.params = {'w': rng.normal(size=(inputs, hidden))/np.sqrt(inputs),
                           'b': np.zeros(hidden),
                           'v': rng.normal(size=hidden)/np.sqrt(hidden),
                           'c': np.zeros(1)}
        else:
            self.params = {'w': rng.normal(size=inputs)/np.sqrt(inputs),
                           'b': np.zeros(1)}

    def __call__(self, x):
        p = self.params
        if not self.hidden:
            return x @ p['w'] + p['b'][0]
        return np.tanh(x @ p['w'] + p['b']) @ p['v'] + p['c'][0]

    def backward(self, x, dz):
        p = self.params
        if not self.hidden:
            return {'w': x.T @ dz, 'b': np.array([dz.sum()])}
        h = np.tanh(x @ p['w'] + p['b'])
        dh = dz[:, None]*p['v']*(1-h*h)
        return {'w': x.T @ dh, 'b': dh.sum(axis=0),
                'v': h.T @ dz, 'c': np.array([dz.sum()])}


def supervised_loss_grad(model, x, y):
    z = model(x)
    return float(np.mean(np.logaddexp(0, z)-y*z)), model.backward(
        x, (sigmoid(z)-y)/len(y))


def joint_loss_grad(sender, receiver, s, q, y):
    """Enumerate both hard symbols; never feed a real-valued message to reader."""
    p = sigmoid(sender(s))
    xm = np.c_[-np.ones(len(y)), q]
    xp = np.c_[np.ones(len(y)), q]
    zm, zp = receiver(xm), receiver(xp)
    lm, lp = np.logaddexp(0, zm)-y*zm, np.logaddexp(0, zp)-y*zp
    gs = sender.backward(s, (lp-lm)*p*(1-p)/len(y))
    gm = receiver.backward(xm, (1-p)*(sigmoid(zm)-y)/len(y))
    gp = receiver.backward(xp, p*(sigmoid(zp)-y)/len(y))
    return float(np.mean((1-p)*lm+p*lp)), gs, {k: gm[k]+gp[k] for k in gm}


class Adam:
    def __init__(self, model, lr):
        self.params, self.lr, self.t = model.params, lr, 0
        self.m = {k: np.zeros_like(v) for k, v in self.params.items()}
        self.v = {k: np.zeros_like(v) for k, v in self.params.items()}

    def step(self, grads):
        self.t += 1
        for k, p in self.params.items():
            g = grads[k]
            self.m[k] = .9*self.m[k]+.1*g
            self.v[k] = .999*self.v[k]+.001*g*g
            p -= self.lr*(self.m[k]/(1-.9**self.t))/(
                np.sqrt(self.v[k]/(1-.999**self.t))+1e-8)


def fit(model, x, y, steps, lr):
    opt = Adam(model, lr)
    for _ in range(steps):
        _, grads = supervised_loss_grad(model, x, y)
        opt.step(grads)


def accuracies(pred, d):
    correct = pred == d['y']
    return {'train': float(correct[d['train']].mean()),
            'test': float(correct[~d['train']].mean()),
            'full': float(correct.mean())}


def evaluate(sender, receiver, d):
    s, q, y, w, train = (d[k] for k in ('s', 'q', 'y', 'w', 'train'))
    prob = sigmoid(sender(s))
    m = np.where(prob >= .5, 1., -1.)

    def predict(message):
        return receiver(np.c_[message, q]) >= 0

    predictions = predict(m)
    metrics = accuracies(predictions, d)
    aligned = float(np.mean(m == w))
    metrics['rule_alignment'] = max(aligned, 1-aligned)
    opposite = s.copy()
    opposite[:, 2] *= -1
    opposite_m = np.where(sender(opposite) >= 0, 1., -1.)
    interventions = {'erased': np.zeros(len(y)), 'flipped': -m,
                     'opposite_world': opposite_m}
    intervention_predictions = {k: predict(v) for k, v in interventions.items()}
    for key, pred in intervention_predictions.items():
        metrics[key] = float(np.mean(pred[~train] == y[~train]))
    metrics['random'] = float(sum(np.mean(predict(np.full(len(y), sign))[~train]
                                         == y[~train]) for sign in (-1, 1))/2)
    cases = []
    for i in range(len(y)):
        cases.append({'source': s[i].astype(int).tolist(),
                      'query': q[i].astype(int).tolist(), 'world': int(w[i]),
                      'target': int(2*y[i]-1), 'split': 'train' if train[i] else 'test',
                      'message': int(m[i]), 'message_p_plus': float(prob[i]),
                      'prediction': int(2*int(predictions[i])-1),
                      **{k+'_prediction': int(2*int(v[i])-1)
                         for k, v in intervention_predictions.items()}})
    return metrics, cases


def run_seed(seed, steps=5000, lr=.01):
    d = dataset()
    s, q, y = (d[k][d['train']] for k in ('s', 'q', 'y'))
    rng = np.random.default_rng(seed)
    sender, receiver = MLP(3, 16, rng), MLP(3, 16, rng)
    so, ro = Adam(sender, lr), Adam(receiver, lr)
    for _ in range(steps):
        _, gs, gr = joint_loss_grad(sender, receiver, s, q, y)
        so.step(gs)
        ro.step(gr)
    joint, cases = evaluate(sender, receiver, d)
    fresh = MLP(3, 16, np.random.default_rng(seed+10000))
    fit(fresh, np.c_[np.where(sender(s) >= 0, 1., -1.), q], y, steps, lr)
    fresh_metrics, fresh_cases = evaluate(sender, fresh, d)
    direct = MLP(5, 23, np.random.default_rng(seed+20000))
    linear = MLP(5, 0, np.random.default_rng(seed+30000))
    full_x = np.c_[d['s'], d['q']]
    baselines = {}
    for name, model in (('direct', direct), ('linear', linear)):
        fit(model, full_x[d['train']], y, steps, lr)
        baselines[name] = accuracies(model(full_x) >= 0, d)
        for row, pred in zip(cases, model(full_x) >= 0):
            row[name+'_prediction'] = int(2*int(pred)-1)
    weights = {name+'_'+k: v for name, model in
               (('sender', sender), ('receiver', receiver), ('fresh', fresh),
                ('direct', direct), ('linear', linear)) for k, v in model.params.items()}
    result = {'seed': seed, 'joint': joint, 'fresh': fresh_metrics,
              **baselines, 'cases': cases, 'fresh_cases': fresh_cases}
    return result, weights


def verdicts(records, expected=5):
    if len(records) != expected:
        return {'status': 'INCOMPLETE', 'completed': len(records), 'expected': expected}
    def succeeds(m):
        return m['test'] >= .95 and m['full'] >= .95
    g1 = sum(succeeds(r['joint']) for r in records)
    g2 = sum(r['joint']['test'] >= .95 and
             abs(r['joint']['erased']-.5) < 1e-12 and
             abs(r['joint']['random']-.5) < 1e-12 and
             r['joint']['opposite_world'] <= .1 and
             r['joint']['flipped'] <= .1 for r in records)
    g3 = sum(succeeds(r['fresh']) for r in records)
    # Registered threshold is 4/5; nonregistered test runs are explicitly marked.
    return {'status': 'COMPLETE', 'registered_seed_count': expected == 5,
            'G1': 'PASS' if g1 >= 4 else 'FAIL',
            'G2': 'PASS' if g2 >= 4 else 'FAIL',
            'G3': 'PASS' if g3 >= 4 else 'FAIL',
            'G4': 'REPORTED', 'qualifying_seeds': {'G1': g1, 'G2': g2, 'G3': g3}}
