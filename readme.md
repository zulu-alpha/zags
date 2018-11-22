# Zulu-Alpha Game Server

An ephemeral, short lived Arma 3 server that can be quickly run anywhere in the world with mods and easy configuration via environmental variables.
Designed to work with Azure, due it's widest region availability and SMB file servers and windows container support as a backup.

## Environment configuration

These environmental variables are not used to generate config files, but instead other aspects of the server, such as mods.

* **MODLINE**: A string describing which set of mods to use. This string is from a standard [mod-line json file](https://github.com/zulu-alpha/mod-lines).
* **MODS_STORAGE_ACCOUNT_NAME**: Azure storage account name for mods and keys. Ideally it should be in the same Azure region as this container is running in
* **MODS_STORAGE_ACCOUNT_KEY**: Key for the given Azure storage account name.
* **MISSIONS_STORAGE_ACCOUNT_NAME**: Azure storage account name for missions. Ideally it should be in the same Azure region as this container is running in
* **MISSIONS_STORAGE_ACCOUNT_KEY**: Key for the given Azure storage account name.
* **MODS_SHARE_NAME**: Name of the Azure shared directory that the mods will be in.
* **KEYS_SHARE_NAME**: Name of the Azure shared directory that mod's keys will be in.
* **MISSIONS_SHARE_NAME**: Name of the Azure shared directory that missions will be in.

## Configuration file basics

server.cfg, basic.cfg and the server.armaprofile has it's values generated based on global variables available to this container on first start.
If a global variable is not defined then that variable will not be defined at all in the settings file.
There is no validation done outside of Arma itself regarding the values, so if you give invalid values, then look to Arma for an error message.

## Defining arrays

For settings that are arrays, use the delimiter `:` to separate elements.

### For example:

To get `admins[]={"1234","5678"};` in the `server.cfg`, define the environmental variable like so: `CONFIG_ADMINS=1234:5678`

## server.cfg environmental variables

The following environmental variables map onto their associated parameter names, which can be referenced in the official [server.cfg documentation](https://community.bistudio.com/wiki/server.cfg):

* **CONFIG_PASSWORD_ADMIN**: `passwordAdmin`
* **CONFIG_PASSWORD**: `password`
* **CONFIG_SERVER_COMMAND_PASSWORD**: `serverCommandPassword`
* **CONFIG_HOSTNAME**: `hostname`
* **CONFIG_MAX_PLAYERS**: `maxPlayers`
* **CONFIG_MOTD**: `motd[]`
* **CONFIG_ADMINS**: `admins[]`
* **CONFIG_HEADLESS_CLIENTS**: `headlessClients[]`
* **CONFIG_LOCAL_CLIENTS**: `localClient[]`
* **CONFIG_VOTE_THRESHOLD**: `voteThreshold`
* **CONFIG_VOTE_MISSION_PLAYERS**: `voteMissionPlayers`
* **CONFIG_KICK_DUPLICATE**: `kickduplicate`
* **CONFIG_UPNP**: `upnp`
* **CONFIG_ALLOWED_FILE_PATCHING**: `allowedFilePatching`
* **CONFIG_DISCONNECT_TIMEOUT**: `disconnectTimeout`
* **CONFIG_MAX_DESYNC**: `maxdesync`
* **CONFIG_MAX_PING**: `maxping`
* **CONFIG_MAX_PACKETLOSS**: `maxpacketloss`
* **CONFIG_KICK_CLIENTS_ON_SLOW_NETWORK**: `kickClientsOnSlowNetwork[]`
* **CONFIG_VERIFY_SIGNATURES**: `verifySignatures`
* **CONFIG_DRAWING_IN_MAP**: `drawingInMap`
* **CONFIG_DISABLE_VON**: `disableVoN`
* **CONFIG_VON_CODEC_QUALITY**: `vonCodecQuality`
* **CONFIG_VON_CODEC**: `vonCodec`
* **CONFIG_LOG_FILE**: `logFile`
* **CONFIG_DOUBLE_ID_DETECTED**: `doubleIdDetected`
* **CONFIG_ON_USER_CONNECTED**: `onUserConnected`
* **CONFIG_ON_USER_DISCONNECTED**: `onUserDisconnected`
* **CONFIG_ON_HACKED_DATA**: `onHackedData`
* **CONFIG_ON_DIFFERENT_DATA**: `onDifferentData`
* **CONFIG_ON_UNSIGNED_DATA**: `onUnsignedData`
* **CONFIG_REGULAR_CHECK**: `regularCheck`
* **CONFIG_BATTLEYE**: `BattlEye`
* **CONFIG_BATTLEYE_LICENSE**: `battleyeLicense`
* **CONFIG_TIME_STAMP_FORMAT**: `timeStampFormat`
* **CONFIG_FORCE_ROTORLIB_SIMULATION**: `forceRotorLibSimulation`
* **CONFIG_PERSISTENT**: `persistent`
* **CONFIG_FORCED_DIFFICULTY**: `forcedDifficulty`
* **CONFIG_REQUIRED_BUILD**: `requiredBuild`
* **CONFIG_MISSION_WHITELIST**: `missionWhitelist[]`

### Mission rotation environmental variables

The following environmental variables are different, in that they define the mission rotation class in the `server.cfg`.
These are each arrays and the nth element of each array represents the nth mission defined in the `server.cfg` file:

* **CONFIG_MISSION_ROTATION_CLASSNAMES**
* **CONFIG_MISSION_ROTATION_NAMES**
* **CONFIG_MISSION_ROTATION_DIFFICULTIES**
* **CONFIG_MISSION_ROTATION_PARAMS**

#### For example

* `CONFIG_MISSION_ROTATION_CLASSNAMES=Mission1:Mission2`
* `CONFIG_MISSION_ROTATION_NAMES=co@12_opsalamander_v1-2-0.Tanoa:zat_selection_v2-1-0.Malden`
* `CONFIG_MISSION_ROTATION_DIFFICULTIES=Custom:veteran`
* `CONFIG_MISSION_ROTATION_PARAMS=someparam:otherparam`

Will give:
```c
class Missions
{

	class Mission1
	{
		template = co@12_opsalamander_v1-2-0.Tanoa;
		difficulty = "Custom";
		class Params { someparam };
	};
	class Mission2
	{
		template = zat_selection_v2-1-0.Malden;
		difficulty = "veteran";
		class Params { otherparam };
	};
	
};
```
Note that the `.pbo` is not included for the mission files (`template`)
Also note that if one mission rotation variable is provided, then you need to provide them all, except for `CONFIG_MISSION_ROTATION_PARAMS`, which is still optional

## basic.cfg environmental variables

The following environmental variables map onto their associated parameter names, which can be referenced in the official [basic.cfg documentation](https://community.bistudio.com/wiki/basic.cfg):

* **BASIC_MAX_MSG_SEND**: `MaxMsgSend`
* **BASIC_SIZE_GUARANTEED**: `MaxSizeGuaranteed`
* **BASIC_MAX_SIZE_NONGUARANTEED**: `MaxSizeNonguaranteed`
* **BASIC_MIN_BANDWIDTH**: `MinBandwidth`
* **BASIC_MAX_BANDWIDTH**: `MaxBandwidth`
* **BASIC_MIN_ERROR_TO_SEND**: `MinErrorToSend`
* **BASIC_MIN_ERROR_TO_SEND_NEAR**: `MinErrorToSendNear`
* **BASIC_MAX_PACKET_SIZE**: `maxPacketSize`
* **BASIC_MAX_CUSTOM_FILE_SIZE**: `MaxCustomFileSize`

## server.armaprofile environmental variables

The following environmental variables map onto their associated parameter names, which can be referenced in the official [server.armaprofile documentation](https://community.bistudio.com/wiki/server.armaprofile#Arma_3):

* **PROFILE_REDUCED_DAMAGE**: `reducedDamage`
* **PROFILE_GROUP_INDICATORS**: `groupIndicators`
* **PROFILE_FRIENDLY_TAGS**: `friendlyTags`
* **PROFILE_ENEMY_TAGS**: `enemyTags`
* **PROFILE_DETECTED_MINES**: `detectedMines`
* **PROFILE_COMMANDS**: `commands`
* **PROFILE_WAYPOINTS**: `waypoints`
* **PROFILE_TACTICAL_PING**: `tacticalPing`
* **PROFILE_WEAPON_INFO**: `weaponInfo`
* **PROFILE_STANCE_INDICATOR**: `stanceIndicator`
* **PROFILE_STAMINA_BAR**: `staminaBar`
* **PROFILE_WEAPON_CROSSHAIR**: `weaponCrosshair`
* **PROFILE_VISION_AID**: `visionAid`
* **PROFILE_THIRD_PERSON_VIEW**: `thirdPersonView`
* **PROFILE_CAMERA_SHAKE**: `cameraShake`
* **PROFILE_SCORE_TABLE**: `scoreTable`
* **PROFILE_DEATH_MESSAGE**: `deathMessages`
* **PROFILE_VON_ID**: `vonID`
* **PROFILE_MAP_CONTENT**: `mapContent`
* **PROFILE_AUTO_REPORT**: `autoReport`
* **PROFILE_MULTIPLE_SAVES**: `multipleSaves`
* **PROFILE_AI_LEVEL_PRESET**: `aiLevelPreset`
* **PROFILE_CUSTOM_AI_LEVEL_SKILL_AI**: `skillAI`
* **PROFILE_CUSTOM_AI_LEVEL_PRECISION_AI**: `precisionAI`
