#include <unordered_map>
#include "stdio.h"
#include "defs.h"

using namespace std;


unordered_map<U64, S_HASHENTRY> wordMap;

// void InitHashTable() {

// 	int HashSize = 0x100000 * MB;
//     table->numEntries = HashSize / sizeof(S_HASHENTRY);
//     table->numEntries -= 2;
// 	if(table->pTable!=NULL) {
// 		free(table->pTable);
// 	}

//     table->pTable = (S_HASHENTRY *) malloc(table->numEntries * sizeof(S_HASHENTRY));
// 	if(table->pTable == NULL) {
// 		printf("Hash Allocation Failed, trying %dMB...\n",MB/2);
// 		InitHashTable(table,MB/2);
// 	} else {
// 		ClearHashTable(table);
// 		printf("HashTable init complete with %d entries\n",table->numEntries);
// 	}
// }