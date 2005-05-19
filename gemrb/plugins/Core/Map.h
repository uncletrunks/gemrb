/* GemRB - Infinity Engine Emulator
 * Copyright (C) 2003 The GemRB Project
 *
 * This program is free software; you can redistribute it and/or
 * modify it under the terms of the GNU General Public License
 * as published by the Free Software Foundation; either version 2
 * of the License, or (at your option) any later version.

 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.

 * You should have received a copy of the GNU General Public License
 * along with this program; if not, write to the Free Software
 * Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA  02111-1307, USA.
 *
 * $Header: /data/gemrb/cvs2svn/gemrb/gemrb/gemrb/plugins/Core/Map.h,v 1.72 2005/05/19 14:56:18 avenger_teambg Exp $
 *
 */

class Map;

#ifndef MAP_H
#define MAP_H

#include "TileMap.h"
#include "ImageMgr.h"
#include "Actor.h"
#include "ScriptedAnimation.h"
#include "GameControl.h"
#include "PathFinder.h"
#include <queue>

class Ambient;

#ifdef WIN32

#ifdef GEM_BUILD_DLL
#define GEM_EXPORT __declspec(dllexport)
#else
#define GEM_EXPORT __declspec(dllimport)
#endif

#else
#define GEM_EXPORT
#endif

//area types
#define AT_EXTENDED_NIGHT  0x40
#define AT_CAN_REST        0x80

//area animation flags
#define A_ANI_ACTIVE          1        //if not set, animation is invisible
#define A_ANI_NO_SHADOW       2        //lightmap doesn't affect it
#define A_ANI_BLEND           4        //blend
#define A_ANI_PLAYONCE        8        //stop after endframe
#define A_ANI_SYNC            16       //synchronised draw (skip frames if needed)
#define A_ANI_32              32
#define A_ANI_NO_WALL         64       //draw after walls (walls don't cover it)
#define A_ANI_NOT_IN_FOG      0x80     //not visible in fog of war
#define A_ANI_BACKGROUND      0x100    //draw before actors (actors cover it)
#define A_ANI_ALLCYCLES       0x200    //draw all cycles, not just the cycle specified
#define A_ANI_PALETTE         0x400    //has own palette set
#define A_ANI_MIRROR          0x800    //mirrored
#define A_ANI_COMBAT          0x1000   //draw in combat too

//creature area flags
#define AF_CRE_NOT_LOADED 1
#define AF_NAME_OVERRIDE  8

//getline flags
#define GL_NORMAL         0
#define GL_PASS           1
#define GL_REBOUND        2

typedef struct SongHeaderType {
	ieDword SongList[5];
} SongHeaderType;

typedef struct RestHeaderType {
	ieDword Strref[10];
	ieResRef CreResRef[10];
	ieWord CreatureNum;
	ieWord DayChance;
	ieWord NightChance;
} RestHeaderType;

typedef struct WallGroup {
	Gem_Polygon** polys;
	int polygons;
} WallGroup;

typedef struct Entrance {
	char Name[33];
	Point Pos;
	ieDword Face;
} Entrance;

typedef class MapNote {
public:
	Point Pos;
	ieWord color;
	char *text;
	MapNote() { text=NULL; };
	~MapNote() { if(text) free(text); };
} MapNote;

class GEM_EXPORT Map : public Scriptable {
public:
	TileMap* TMap;
	ImageMgr* LightMap;
	ImageMgr* SearchMap;
	ImageMgr* SmallMap;
	ieDword AreaFlags;
	ieWord AreaType;
	bool ChangeArea; //set true if movement is allowed between areas
	Variables *vars;
	ieByte* ExploredBitmap;
	ieByte* VisibleBitmap;
private:
	unsigned short* MapSet;
	std::queue< unsigned int> InternalStack;
	unsigned int Width, Height;
	std::vector< Animation*> animations;
	std::vector< Actor*> actors;
	std::vector< WallGroup*> wallGroups;
	std::vector< ScriptedAnimation*> vvcCells;
	std::vector< Entrance*> entrances;
	std::vector< Ambient*> ambients;
	std::vector< MapNote*> mapnotes;
	Actor** queue[3];
	int Qcount[3];
	unsigned int lastActorCount[3];
public:
	Map(void);
	~Map(void);
	/** prints useful information on console */
	void DebugDump();
	void AddTileMap(TileMap* tm, ImageMgr* lm, ImageMgr* sr, ImageMgr* sm);
	void CreateMovement(char *command, const char *area, const char *entrance);
	void UpdateScripts();
	void DrawContainers(Region screen, Container *overContainer);
	void DrawMap(Region screen, GameControl* gc);
	void PlayAreaSong(int);
	void AddAnimation(Animation* anim);
	Animation* GetAnimation(const char* Name);
	void Shout(Scriptable* Sender, int shoutID, unsigned int radius);
	void AddActor(Actor* actor);
	void AddWallGroup(WallGroup* wg);
	int GetBlocked(Point &p);
	Actor* GetActor(Point &p, int flags);
	Actor* GetActor(const char* Name);
	Actor* GetActorByDialog(const char* resref);
	bool HasActor(Actor *actor);
	void RemoveActor(Actor* actor);
	//returns actors in rect (onlyparty could be more sophisticated)
	int GetActorInRect(Actor**& actors, Region& rgn, bool onlyparty);
	SongHeaderType SongHeader;
	RestHeaderType RestHeader;
	void AddVVCCell(ScriptedAnimation* vvc);
	void AddEntrance(char* Name, int XPos, int YPos, short Face);
	Entrance* GetEntrance(const char* Name);
	bool CanFree();
	Actor* GetActor(int i) { return actors[i]; }
	int GetActorCount() const { return (int) actors.size(); }
	int GetWidth() const { return Width; }
	int GetHeight() const { return Height; }
	int GetExploredMapSize() const;
	/*fills the explored bitmap with setreset */
	void Explore(int setreset);
	/*fills the visible bitmap with setreset */
	void SetMapVisibility(int setreset = 0);
	/* set one fog tile as visible. x, y are tile coordinates */
	void ExploreTile(Point &Tile);
	/* explore map from given point in map coordinates */
	void ExploreMapChunk(Point &Pos, int range, bool los);
	/* update VisibleBitmap by resolving vision of all explore actors */
	void UpdateFog();
	//PathFinder
	/* Finds the nearest passable point */
	void AdjustPosition(Point &goal, unsigned int radius=0);
	/* Jumps actors out of impassable areas, call this after a searchmap change */
	void FixAllPositions();
	/* Finds the path which leads the farthest from d */
	PathNode* RunAway(Point &s, Point &d, unsigned int PathLen, int flags);
	/* Returns true if there is no path to d */
	bool TargetUnreachable(Point &s, Point &d);
	/* Finds straight path from s, length l and orientation o, f=1 passes wall, f=2 rebounds from wall*/
	PathNode* GetLine(Point &start, int Steps, int Orientation, int flags);
	PathNode* GetLine(Point &start, Point &dest, int flags);
	/* Finds the path which leads to d */
	PathNode* FindPath(Point &s, Point &d);
	/* returns false if point isn't visible on visibility/explored map */
	bool IsVisible(Point &s, int explored);
	/* returns false if point d cannot be seen from point d due to searchmap */
	bool IsVisible(Point &s, Point &d);
	/* returns edge direction of map boundary, only worldmap regions */
	int WhichEdge(Point &s);

	//ambients
	void AddAmbient(Ambient *ambient) { ambients.push_back(ambient); }
	void SetupAmbients();

	//mapnotes
	void AddMapNote(Point point, int color, char *text);
	void RemoveMapNote(Point point);
	MapNote *GetMapNote(int i) { return mapnotes[i]; }
	MapNote *GetMapNote(Point point);
	unsigned int GetMapNoteCount() { return (unsigned int) mapnotes.size(); }

	/* May spawn creature(s), returns true in case of an interrupted rest */
	bool Rest(Point pos, int hours);
	/* Spawns creature(s) in radius of position */
	void SpawnCreature(Point pos, char *CreName, int radius = 0);
private:
	void GenerateQueues();
	Actor* GetRoot(int priority, int &index);
	void DeleteActor(int i);
	void Leveldown(unsigned int px, unsigned int py, unsigned int& level,
		Point &p, unsigned int& diff);
	void SetupNode(unsigned int x, unsigned int y, unsigned int Cost);
	//maybe this is unneeded and orientation could be calculated on the fly
	void UseExit(Actor *pc, InfoPoint *ip);
	bool HandleActorStance(Actor *actor, CharAnimations *ca, int StanceID);
	PathNode* GetLine(Point &start, Point &dest, int Steps, int Orientation, int flags);
};

#endif
