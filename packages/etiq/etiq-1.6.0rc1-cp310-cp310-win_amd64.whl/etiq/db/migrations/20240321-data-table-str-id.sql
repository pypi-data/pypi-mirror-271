-- Data Table id column should be a string uuid not an int

PRAGMA foreign_keys=off;

DROP TABLE IF EXISTS _data;
CREATE TABLE _data (
    id TEXT PRIMARY KEY,
    name TEXT,
    hash TEXT
);

DROP TABLE IF EXISTS _data_mapping;
CREATE TABLE _data_mapping (
    old_id INT,
    id TEXT
);

INSERT INTO _data_mapping (old_id, id)
SELECT id, shortuuid()
FROM data;

INSERT INTO _data (id, name, hash)
SELECT _data_mapping.id, data.name, data.hash
FROM data
LEFT JOIN _data_mapping ON _data_mapping.old_id = data.id;

-- dataconfig (data_id column is already varchar)
UPDATE dataconfig
SET data_id = (
    SELECT _data_mapping.id
    FROM _data_mapping
    WHERE _data_mapping.old_id = dataconfig.id
);

-- snapshot
DROP TABLE IF EXISTS _snapshot;
CREATE TABLE _snapshot (
	id VARCHAR NOT NULL,
	pipeline_id VARCHAR,
	run_id VARCHAR,
	created TIMESTAMP,
	name VARCHAR,
	project_id VARCHAR,
	model_id VARCHAR,
	data_id VARCHAR,
	comparison_data_id VARCHAR,
	stage VARCHAR(14),
	status VARCHAR(7),
	significant_features VARCHAR,
	meta JSON,
	PRIMARY KEY (id),
	FOREIGN KEY(project_id) REFERENCES project (id),
	FOREIGN KEY(model_id) REFERENCES model (id),
	FOREIGN KEY(data_id) REFERENCES data (id),
	FOREIGN KEY(comparison_data_id) REFERENCES data (id)
);

INSERT INTO _snapshot (
	id,
	pipeline_id,
	run_id,
	created,
	name,
	project_id,
	model_id,
	data_id,
	comparison_data_id,
	stage,
	status,
	significant_features,
	meta
	)
SELECT
	id,
	pipeline_id,
	run_id,
	created,
	name,
	project_id,
	model_id,
	data_id,
	comparison_data_id,
	stage,
	status,
	significant_features,
	meta
 FROM snapshot;

UPDATE _snapshot SET data_id = (
	SELECT _data_mapping.id FROM _data_mapping WHERE _data_mapping.old_id = _snapshot.data_id
);
UPDATE _snapshot SET comparison_data_id = (
	SELECT _data_mapping.id FROM _data_mapping WHERE _data_mapping.old_id = _snapshot.comparison_data_id
);

DROP TABLE snapshot;
ALTER TABLE _snapshot RENAME TO snapshot;
DROP TABLE data;
ALTER TABLE _data RENAME TO data;
DROP TABLE _data_mapping;

PRAGMA foreign_keys=on;
