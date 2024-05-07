import r from '@hat-open/renderer';
import * as u from '@hat-open/util';
import * as juggler from '@hat-open/juggler';
const defaultState = {
    remote: null
};
let app = null;
function main() {
    const root = document.body.appendChild(document.createElement('div'));
    r.init(root, defaultState, vt);
    app = new juggler.Application('remote');
}
function vt() {
    const remote = r.get('remote');
    if (remote == null)
        return ['div.orchestrator'];
    const components = r.get('remote', 'components');
    return ['div.orchestrator',
        ['table',
            ['thead',
                ['tr',
                    ['th.col-component', 'Component'],
                    ['th.col-delay', 'Delay'],
                    ['th.col-revive', 'Revive'],
                    ['th.col-status', 'Status'],
                    ['th.col-action', 'Action']
                ]
            ],
            ['tbody', components.map(component => ['tr',
                    ['td.col-component', component.name],
                    ['td.col-delay', String(component.delay)],
                    ['td.col-revive',
                        ['input', {
                                props: {
                                    type: 'checkbox',
                                    checked: component.revive
                                },
                                on: {
                                    change: (evt) => {
                                        if (!app)
                                            return;
                                        app.send('revive', {
                                            id: component.id,
                                            value: evt.target.checked
                                        });
                                    }
                                }
                            }
                        ]
                    ],
                    ['td.col-status', component.status],
                    ['td.col-action',
                        ['button', {
                                props: {
                                    title: 'Stop',
                                    disabled: u.contains(component.status, ['STOPPING', 'STOPPED'])
                                },
                                on: {
                                    click: () => {
                                        if (!app)
                                            return;
                                        app.send('stop', {
                                            id: component.id
                                        });
                                    }
                                }
                            },
                            icon('media-playback-stop')
                        ],
                        ['button', {
                                props: {
                                    title: 'Start',
                                    disabled: u.contains(component.status, ['STARTING', 'RUNNING', 'STOPPING'])
                                },
                                on: {
                                    click: () => {
                                        if (!app)
                                            return;
                                        app.send('start', {
                                            id: component.id
                                        });
                                    }
                                }
                            },
                            icon('media-playback-start')
                        ]
                    ]])]
        ]
    ];
}
function icon(name) {
    return ['img.icon', {
            props: {
                src: `icons/${name}.svg`
            }
        }];
}
window.addEventListener('load', main);
window.r = r;
window.u = u;
