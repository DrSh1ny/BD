drop table pessoa cascade;
drop table artigo cascade;
drop table historico cascade;
drop table leilao cascade;
drop table licitacao cascade;
drop table mensagem cascade;
drop table notificacao cascade;
drop table notificacao_pessoa cascade;

CREATE TABLE pessoa (
	id	 serial,
	nome	 VARCHAR(512) UNIQUE NOT NULL,
	password	 VARCHAR(512) NOT NULL,
	email	 VARCHAR(512),
	auth_token VARCHAR(512),
	exp_date	 TIMESTAMP,
	PRIMARY KEY(id)
);

CREATE TABLE artigo (
	codigo BIGINT,
	PRIMARY KEY(codigo)
);

CREATE TABLE leilao (
	id		 serial,
	titulo	 VARCHAR(512) NOT NULL,
	descricao	 VARCHAR(512),
	data_inicio	 TIMESTAMP NOT NULL,
	data_fim	 TIMESTAMP NOT NULL,
	preco_inicial INTEGER NOT NULL,
	pessoa_id	 BIGINT NOT NULL,
	artigo_codigo BIGINT NOT NULL,
	PRIMARY KEY(id)
);

CREATE TABLE licitacao (
	preco	 BIGINT NOT NULL,
	data	 TIMESTAMP,
	leilao_id BIGINT,
	pessoa_id BIGINT,
	PRIMARY KEY(data,leilao_id,pessoa_id)
);

CREATE TABLE mensagem (
	titulo	 VARCHAR(512) NOT NULL,
	descricao VARCHAR(512) NOT NULL,
	data	 TIMESTAMP,
	leilao_id BIGINT,
	pessoa_id BIGINT,
	PRIMARY KEY(data,leilao_id,pessoa_id)
);

CREATE TABLE historico (
	data_alteracao TIMESTAMP NOT NULL,
	titulo	 VARCHAR(512) NOT NULL,
	descricao	 VARCHAR(512),
	leilao_id	 BIGINT,
	PRIMARY KEY(leilao_id)
);

CREATE TABLE notificacao_pessoa (
	lida		 BOOL NOT NULL,
	notificacao_data TIMESTAMP,
	pessoa_id	 BIGINT,
	PRIMARY KEY(notificacao_data,pessoa_id)
);

CREATE TABLE notificacao (
	mensagem VARCHAR(512) NOT NULL,
	data	 TIMESTAMP,
	PRIMARY KEY(data)
);

ALTER TABLE leilao ADD CONSTRAINT leilao_fk1 FOREIGN KEY (pessoa_id) REFERENCES pessoa(id);
ALTER TABLE leilao ADD CONSTRAINT leilao_fk2 FOREIGN KEY (artigo_codigo) REFERENCES artigo(codigo);
ALTER TABLE licitacao ADD CONSTRAINT licitacao_fk1 FOREIGN KEY (leilao_id) REFERENCES leilao(id);
ALTER TABLE licitacao ADD CONSTRAINT licitacao_fk2 FOREIGN KEY (pessoa_id) REFERENCES pessoa(id);
ALTER TABLE mensagem ADD CONSTRAINT mensagem_fk1 FOREIGN KEY (leilao_id) REFERENCES leilao(id);
ALTER TABLE mensagem ADD CONSTRAINT mensagem_fk2 FOREIGN KEY (pessoa_id) REFERENCES pessoa(id);
ALTER TABLE historico ADD CONSTRAINT historico_fk1 FOREIGN KEY (leilao_id) REFERENCES leilao(id);
ALTER TABLE notificacao_pessoa ADD CONSTRAINT notificacao_pessoa_fk1 FOREIGN KEY (notificacao_data) REFERENCES notificacao(data);
ALTER TABLE notificacao_pessoa ADD CONSTRAINT notificacao_pessoa_fk2 FOREIGN KEY (pessoa_id) REFERENCES pessoa(id);