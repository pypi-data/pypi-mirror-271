from AlgoGrade.core import Scoring
from AlgoGrade.preparata import PreparataAnswers, PreparataGrader


scorings = [
    Scoring(max_grade=0.25, fine=0.25),
    Scoring(max_grade=0.25, fine=0.25, repeat_fine=1.5),
    Scoring(max_grade=0.25, fine=0.25, repeat_fine=1),
    Scoring(max_grade=0.25, fine=0.25, repeat_fine=1.5)
]


def test_prep():
    answers = PreparataAnswers(**{
        "tree": {
            "root": {
                "data": {
                    "coords": [
                        3,
                        3
                    ]
                },
                "left": {
                    "data": {
                        "coords": [
                            0,
                            0
                        ]
                    },
                    "next": 1,
                    "prev": 2
                },
                "right": {
                    "data": {
                        "coords": [
                            7,
                            0
                        ]
                    },
                    "prev": 1,
                    "next": 0
                },
                "prev": 0,
                "next": 2
            }
        },
        "hull": [
            {
                "coords": [
                    0,
                    0
                ]
            },
            {
                "coords": [
                    3,
                    3
                ]
            },
            {
                "coords": [
                    7,
                    0
                ]
            }
        ],
        "trees": [
            {
                "root": {
                    "data": {
                        "coords": [
                            7,
                            9
                        ]
                    },
                    "left": {
                        "data": {
                            "coords": [
                                0,
                                0
                            ]
                        },
                        "next": 1,
                        "prev": 2
                    },
                    "right": {
                        "data": {
                            "coords": [
                                7,
                                0
                            ]
                        },
                        "prev": 1,
                        "next": 0
                    },
                    "prev": 0,
                    "next": 2
                }
            }
        ],
        "hulls": [
            [
                {
                    "coords": [
                        0,
                        0
                    ]
                },
                {
                    "coords": [
                        7,
                        9
                    ]
                },
                {
                    "coords": [
                        7,
                        0
                    ]
                }
            ],
            [
                {
                    "coords": [
                        0,
                        0
                    ]
                },
                {
                    "coords": [
                        7,
                        9
                    ]
                },
                {
                    "coords": [
                        10,
                        8
                    ]
                },
                {
                    "coords": [
                        7,
                        0
                    ]
                }
            ]
        ],
        "left_paths": [
            [
                "right"
            ],
            [
                "right"
            ]
        ],
        "right_paths": [
            [
                "left"
            ],
            []
        ],
        "left_supporting_points": [
            {
                "coords": [
                    7,
                    0
                ]
            },
            {
                "coords": [
                    7,
                    0
                ]
            }
        ],
        "right_supporting_points": [
            {
                "coords": [
                    0,
                    0
                ]
            },
            {
                "coords": [
                    7,
                    9
                ]
            }
        ],
        "deleted_points_lists": [
            [
                {
                    "coords": [
                        3,
                        3
                    ]
                }
            ],
            []
        ]
    })
    correct_answers = PreparataAnswers(**{
            "hull": [
                {
                    "coords": [
                        0.0,
                        0.0
                    ]
                },
                {
                    "coords": [
                        3.0,
                        3.0
                    ]
                },
                {
                    "coords": [
                        7.0,
                        0.0
                    ]
                }
            ],
            "tree": {
                "root": {
                    "data": {
                        "coords": [
                            3.0,
                            3.0
                        ]
                    },
                    "left": {
                        "data": {
                            "coords": [
                                0.0,
                                0.0
                            ]
                        },
                        "left": None,
                        "right": None,
                        "prev": 2,
                        "next": 1
                    },
                    "right": {
                        "data": {
                            "coords": [
                                7.0,
                                0.0
                            ]
                        },
                        "left": None,
                        "right": None,
                        "prev": 1,
                        "next": 0
                    },
                    "prev": 0,
                    "next": 2
                }
            },
            "left_paths": [
                [
                    "right"
                ],
                [
                    "right"
                ]
            ],
            "right_paths": [
                [
                    "left"
                ],
                []
            ],
            "left_supporting_points": [
                {
                    "coords": [
                        7.0,
                        0.0
                    ]
                },
                {
                    "coords": [
                        7.0,
                        0.0
                    ]
                }
            ],
            "right_supporting_points": [
                {
                    "coords": [
                        0.0,
                        0.0
                    ]
                },
                {
                    "coords": [
                        7.0,
                        9.0
                    ]
                }
            ],
            "deleted_points_lists": [
                [
                    {
                        "coords": [
                            3.0,
                            3.0
                        ]
                    }
                ],
                []
            ],
            "hulls": [
                [
                    {
                        "coords": [
                            0.0,
                            0.0
                        ]
                    },
                    {
                        "coords": [
                            7.0,
                            9.0
                        ]
                    },
                    {
                        "coords": [
                            7.0,
                            0.0
                        ]
                    }
                ],
                [
                    {
                        "coords": [
                            0.0,
                            0.0
                        ]
                    },
                    {
                        "coords": [
                            7.0,
                            9.0
                        ]
                    },
                    {
                        "coords": [
                            10.0,
                            8.0
                        ]
                    },
                    {
                        "coords": [
                            7.0,
                            0.0
                        ]
                    }
                ]
            ],
            "trees": [
                {
                    "root": {
                        "data": {
                            "coords": [
                                7.0,
                                9.0
                            ]
                        },
                        "left": {
                            "data": {
                                "coords": [
                                    0.0,
                                    0.0
                                ]
                            },
                            "left": None,
                            "right": None,
                            "prev": 2,
                            "next": 1
                        },
                        "right": {
                            "data": {
                                "coords": [
                                    7.0,
                                    0.0
                                ]
                            },
                            "left": None,
                            "right": None,
                            "prev": 1,
                            "next": 0
                        },
                        "prev": 0,
                        "next": 2
                    }
                }
            ]
        }
    )

    score, _ = PreparataGrader.grade_answers_wrapper(answers, correct_answers, scorings)
    pass