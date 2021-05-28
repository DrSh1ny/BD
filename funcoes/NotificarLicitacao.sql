CREATE OR REPLACE FUNCTION notifyOnLicitation()
	RETURNS TRIGGER
LANGUAGE 'plpgsql'
AS $BODY$
declare
	f record;
	f1 record;
	msg text;
	dt TIMESTAMP;
	idNotificacao bigint;
	c1 cursor(idLeilao bigint) for
        select *
		from licitacao
		where licitacao.leilao_id=idLeilao and licitacao.preco=(select max(preco) from licitacao where licitacao.leilao_id=idLeilao);
	c2 cursor(idPessoa bigint) for
        select *
        from pessoa
        where pessoa.id=idPessoa;
begin
    open c1(new.leilao_id);
	fetch c1 into f;
	if(not found) then
		return new;
	end if;
	close c1;
	open c2(new.pessoa_id);
	fetch c2 into f1;
	close c2;
	msg:='O licitador ' || f1.nome || ' fez uma licitacao superior a sua no leilao ' || new.leilao_id || ': ' || new.preco;
	dt:= CURRENT_TIMESTAMP;
	insert into notificacao(mensagem,data) values (msg,dt) returning id into idNotificacao;
	insert into notificacao_pessoa(lida,pessoa_id,notificacao_id) values(FALSE,f.pessoa_id,idNotificacao);
	return new;
end;
$BODY$;

DROP TRIGGER IF EXISTS notifyOnLicitation
  ON licitacao;
CREATE TRIGGER notifyOnLicitation 
   before insert
   ON licitacao
   FOR EACH ROW
       EXECUTE PROCEDURE notifyOnLicitation();