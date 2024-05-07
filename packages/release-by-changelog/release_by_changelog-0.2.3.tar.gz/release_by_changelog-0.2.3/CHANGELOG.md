# Changelog

All notable changes to this job will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

[![Pipeline](https://lab.frogg.it/swepy/release-by-changelog/badges/trunk/pipeline.svg)](https://lab.frogg.it/swepy/release-by-changelog/-/pipelines?ref=trunk)

### Planned

#### Changed

* Help options grouping to be more readable.

#### Added

* Add a `--date` option to specify the date of the release, overriding the date of the
  CHANGELOG.md entry.
  A release with a date in the future is labeled as
  an [Upcoming Release](https://lab.frogg.it/help/user/project/releases/index#upcoming-releases).
  A release with a date in the past is labeled as
  a [Historical releases](https://lab.frogg.it/help/user/project/releases/index#historical-releases).
* Add a `--dry-run` option to test the release process without actually releasing a new
  version. Equivalent to automatically reply `no` to the confirmation prompt.
* Add a `--force` option to force the release of a new version even if the version
  already exists, replacing the tag and the release. This is forbidden by SemVers 2, so
  it will require a confirmation prompt, except when using the `--no-interact` option.
* Add a `--message` option to specify the message of the release. Will be used as the
  description of the release, overriding the CHANGELOG.md content.
* Add a `--name` option to specify the name of the release. It will be used right after
  the version in the release title.
* Add a `--prefix` option to specify the prefix of the tag to create.
* Add a `--quiet` option to suppress all output except errors.
* Add a `--rollback` option to roll back the last release.
* Add a `--suffix` option to specify the suffix of the tag to create.
* Add a `--version` option to specify the version to release.

## [0.2.3] - 2024-05-06

[![Pipeline](https://lab.frogg.it/swepy/release-by-changelog/badges/0.2.3/pipeline.svg)](https://lab.frogg.it/swepy/release-by-changelog/-/pipelines?ref=0.2.3)

### Fixed

* Release description is now set to the content of the CHANGELOG.md entry.

## [0.2.2] - 2024-05-06

[![Pipeline](https://lab.frogg.it/swepy/release-by-changelog/badges/0.2.2/pipeline.svg)](https://lab.frogg.it/swepy/release-by-changelog/-/pipelines?ref=0.2.2)

This update only concerns a dependency update.

## [0.2.1] - 2024-05-06

[![Pipeline](https://lab.frogg.it/swepy/release-by-changelog/badges/0.2.1/pipeline.svg)](https://lab.frogg.it/swepy/release-by-changelog/-/pipelines?ref=0.2.1)

This update only concerns a dependency update.

## [0.2.0] - 2024-05-06

[![Pipeline](https://lab.frogg.it/swepy/release-by-changelog/badges/0.2.0/pipeline.svg)](https://lab.frogg.it/swepy/release-by-changelog/-/pipelines?ref=0.2.0)

This update came with more automated tests, a rework of implementation and now, the 
package `release-by-changelog` is now used to release itself.

### Changed

* Error handling

### Added

* Add a `--tag-only` option to create only the tag without creating the release

> Gallius and Iris jump, immediately followed by the seven soldiers of the squad and the
> sergeant, quickly spreading out to form a secure perimeter around the landing zone.
> Through the smoke-saturated air, they scan the surroundings, laser rifles ready for use.
>
> "Regroup!" orders the sergeant over the radio as he heads towards what remains of the
> refinery center. The air is scorching. The smell of promethium fills everyone's nostrils
> despite their masks.
>
> The group advances cautiously, each step measured to avoid unstable ground plates and
> sharp debris. Gallius, leading the way, sweeps the area with his motion detector, with
> Iris and Luther on either side, standing ready.
>
> "Contact at ten o'clock!" yells Gallius, aligning his rifle in the indicated
> direction. All eyes turn towards a pile of twisted metal sheets from which a hirsute and
> grotesque silhouette slowly emerges—an ork. Without hesitation, Luther sends a burst of
> flames towards the creature, which lets out a scream of rage before charging at them,
> the left half of its torso engulfed in deadly flames.
>
> The squad's soldiers, methodical, get into formation in less than 3 seconds. Gallius
> and Iris each fire two shots with terrifying precision at the xeno's knees. The ork
> collapses heavily onto the ground, 3 meters from the squad. Its bulging eyes fixed on
> Gallius's, it rises and lunges at the soldier using only the strength of its arms. Iris
> fires one last time. Less than 6 seconds have elapsed. Only the crackling of the
> green-skin's flesh echoes in the hangar.

## [0.1.0] - 2024-04-28

[![Pipeline](https://lab.frogg.it/swepy/release-by-changelog/badges/0.1.0/pipeline.svg)](https://lab.frogg.it/swepy/release-by-changelog/-/pipelines?ref=0.1.0)

* Initial version

> In the deafening noise of the Valkyrie transport, the troop of Imperial Guards,
> harnessed and armed, finish meticulously preparing their equipment. The atmosphere is
> very humid and hot, stifling. The aircraft skims the dense jungle canopy at an
> astonishing speed, hurtling towards its objective.
>
> "Check your weapons, and keep your eyes wide open. Reports only indicate that the mine
> has been sending distress signals for 20 minutes. We're here only to find out what
> happened, if there's any promethium left to recover, then it's back to base. No
> rescues,
> we're not playing heroes today."
>
> The mechanical voice of the pilot finally announces, "Approaching the extraction zone.
> Deployment in T minus thirty seconds." Each soldier positions themselves, some
> adjusting
> their helmets or fiddling with their comms to reassure themselves, one hand firmly
> gripping the bar. Gallius, whose breathing betrays increasing nervousness, checks the
> mechanism of his laser rifle and glances at his brothers and sisters in arms. Luther
> loads his flamethrower, a small smirk at the corners of his mouth.
>
> The Valkyrie begins its abrupt descent, the turbulence shaking everyone in the cabin.
> As they approach the zone, the ramp lowers, details become visible: gigantic flames
> erupt from fissures in the ground, and partially collapsed structures bear witness to
> a
> violent explosion. "The Emperor protects," mutters Gallius.
>
> "The Emperor protects!" the squad chants in unison. Everyone lowers their gas mask
> over their face.
>
> "We're here. On my signal!" yells the sergeant over the roar of the engines. His
> order, barely audible, is relayed by radio to all squad members.
>
> The Valkyrie stabilizes momentarily above the ground, lifting clouds of dust and
> ashes. The guards are positioned on the ramp. The green light comes on.
>
> "Go!"
